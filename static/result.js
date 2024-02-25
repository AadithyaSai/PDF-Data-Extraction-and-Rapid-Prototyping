const data = JSON.parse(document.getElementById("table_data").textContent);

let content = "";
data.forEach(function (row) {
  content += "<tr>";
  row.forEach(function (cell) {
    content += "<td>" + cell + "</td>";
  });
  content += "</tr>";
});
document.getElementById("table").innerHTML = content;
