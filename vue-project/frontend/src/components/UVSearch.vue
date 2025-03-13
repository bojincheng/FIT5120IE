<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div>
    <input type="date" v-model="searchDate" placeholder="选择日期">
    <input type="number" v-model="searchHour" placeholder="小时" min="0" max="23">
    <input type="number" v-model="searchMinute" placeholder="分钟" min="0" max="59">
    <button @click="fetchData">搜索</button>
    
    <table v-if="results.length > 0">
      <thead>
        <tr>
          <th>Date-Time</th>
          <th>Lat</th>
          <th>Lon</th>
          <th>UV Index</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in results" :key="item.date_time">
          <td>{{ item.date_time }}</td>
          <td>{{ item.lat }}</td>
          <td>{{ item.lon }}</td>
          <td>{{ item.uv_index }}</td>
        </tr>
      </tbody>
    </table>
    <p v-if="results.length === 0 && searchDate">未找到匹配数据</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      searchDate: "", // YYYY-MM-DD
      searchHour: "", // HH
      searchMinute: "", // MM
      results: []
    };
  },
  methods: {
    async fetchData() {
      if (!this.searchDate || this.searchHour === "" || this.searchMinute === "") {
        alert("请输入完整的日期、小时和分钟");
        return;
      }
      try {
        const response = await axios.get(`http://localhost:5000/search`, {
          params: {
            date: this.searchDate,
            hour: String(this.searchHour).padStart(2, '0'), // 补全格式
            minute: String(this.searchMinute).padStart(2, '0')
          }
        });
        this.results = response.data;
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    }
  }
};
</script>

<style scoped>
input {
  margin: 5px;
  padding: 5px;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}
th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}
th {
  background-color: #f4f4f4;
}
</style>
