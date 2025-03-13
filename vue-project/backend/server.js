const express = require('express');
const cors = require('cors');
const { Pool } = require('pg');

const app = express();
app.use(cors()); // 允许跨域
app.use(express.json());

const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'uv_melbourne',
  password: '19991221',
  port: 5432, // PostgreSQL 默认端口
});

// 精确匹配 月-日-时-分 的 API
app.get('/search', async (req, res) => {
  try {
    const { date, hour, minute } = req.query; // 接收前端的查询参数
    console.log("🔍 Received search query:", date, hour, minute);

    const result = await pool.query(
      `SELECT * FROM uv_melbourne 
       WHERE TO_CHAR(date_time, 'YYYY-MM-DD HH24:MI') = $1`,
      [`${date} ${hour}:${minute}`]
    );

    console.log("✅ Query Result:", result.rows);
    res.json(result.rows);
  } catch (err) {
    console.error("❌ Database Query Error:", err);
    res.status(500).send("Server Error");
  }
});

// 启动服务器
app.listen(5000, () => {
  console.log("Server running on port 5000");
});
