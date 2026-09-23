/**
 * importCsv.js
 * Usage: from backend folder run:
 *   npm run import-csv
 *
 * Expects CSV at ../IMDB-Movie-Data.csv (project root)
 */

require('dotenv').config();
const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');
const neo4j = require('neo4j-driver');

const csvPath = path.join(__dirname, '..', 'IMDB-Movie-Data.csv');

const driver = neo4j.driver(
  process.env.NEO4J_URI,
  neo4j.auth.basic(process.env.NEO4J_USER, process.env.NEO4J_PASSWORD),
  { disableLosslessIntegers: true }
);

async function importCsv() {
  const session = driver.session({ defaultAccessMode: neo4j.session.WRITE });

  try {
    console.log('Starting import from:', csvPath);

    const stream = fs.createReadStream(csvPath).pipe(csv());

    for await (const row of stream) {
      // row keys: Ids, Title, Genre, Description, Director, Actors, Year, Runtime, Rating, Votes, Revenue
      const ids = String(row.Ids).trim();
      const title = (row.Title || '').trim();
      const description = (row.Description || '').trim();
      const year = row.Year ? parseInt(row.Year) : null;
      const runtime = row.Runtime ? parseInt(row.Runtime) : null;
      const rating = row.Rating ? parseFloat(row.Rating) : null;
      const votes = row.Votes ? parseInt(row.Votes) : null;
      const revenue = row.Revenue ? parseFloat(row.Revenue) : null;

      // Create / merge Movie node
      const createMovieQuery = `
        MERGE (m:Movie { ids: $ids })
        SET m.title = $title,
            m.description = $description,
            m.year = $year,
            m.runtime = $runtime,
            m.rating = $rating,
            m.votes = $votes,
            m.revenue = $revenue
        RETURN m
      `;

      await session.run(createMovieQuery, {
        ids, title, description, year, runtime, rating, votes, revenue
      });

      // Actors: comma-separated
      const actorsRaw = row.Actors || '';
      const actorNames = actorsRaw.split(',').map(a => a.trim()).filter(a => a.length > 0);
      for (const actorName of actorNames) {
        const q = `
          MERGE (a:Actor { name: $actorName })
          WITH a
          MATCH (m:Movie { ids: $ids })
          MERGE (a)-[:ACTED_IN]->(m)
        `;
        await session.run(q, { actorName, ids });
      }

      // Directors: handle multiple (rare) separated by comma
      const directorsRaw = row.Director || '';
      const directorNames = directorsRaw.split(',').map(d => d.trim()).filter(d => d.length > 0);
      for (const dirName of directorNames) {
        const q = `
          MERGE (d:Director { name: $dirName })
          WITH d
          MATCH (m:Movie { ids: $ids })
          MERGE (d)-[:DIRECTED]->(m)
        `;
        await session.run(q, { dirName, ids });
      }

      // Genres: comma-separated
      const genresRaw = row.Genre || '';
      const genreNames = genresRaw.split(',').map(g => g.trim()).filter(g => g.length > 0);
      for (const gName of genreNames) {
        const q = `
          MERGE (g:Genre { type: $gName })
          WITH g
          MATCH (m:Movie { ids: $ids })
          MERGE (m)-[:IN]->(g)
        `;
        await session.run(q, { gName, ids });
      }
    }

    console.log('CSV import finished.');
  } catch (err) {
    console.error('Import error:', err);
  } finally {
    await session.close();
    await driver.close();
  }
}

importCsv().catch(err => {
  console.error('Fatal import error:', err);
  process.exit(1);
});
