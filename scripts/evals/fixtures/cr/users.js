const express = require('express');
const db = require('./db');
const app = express();
app.get('/user/:id', async (req, res) => {
  const rows = await db.query('SELECT * FROM users WHERE id = ' + req.params.id);
  res.json(rows);
});
app.post('/user/:id/avatar', async (req, res) => {
  const path = '/var/uploads/' + req.query.name;
  require('fs').writeFileSync(path, req.body);
  res.send('ok');
});
app.listen(3000);
