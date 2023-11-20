function convertToCSV(arrayOfObject, addHeader = false) {
  var str = "";

  if (addHeader) {
    var line = "";
    var keyList = Object.keys(arrayOfObject[0]);
    for (var index in keyList) {
      if (line != "") line += ",";
      line += keyList[index];
    }
    str += line + "\r\n";
  }
  for (var i = 0; i < arrayOfObject.length; i++) {
    var line = "";
    var valueList = Object.values(arrayOfObject[i]);
    for (var index in valueList) {
      if (line != "") line += ",";
      line += valueList[index];
    }
    str += line + "\r\n";
  }

  return str;
}

function downloadCSV(pageNumber, csv) {
  var blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
  var a = document.createElement("a");
  a.href = window.URL.createObjectURL(blob);
  a.download = `${pageNumber}.csv`;
  a.click();
}
function downloadJSON(pageNumber, data) {
  const blob = new Blob([JSON.stringify(data)], { type: "text/json" });
  var a = document.createElement("a");
  a.href = window.URL.createObjectURL(blob);
  a.download = `${pageNumber}.json`;
  a.click();
}

function getCurrentPageNumber() {
  var paginator = document.querySelector(
    "body > div.dialog-off-canvas-main-canvas > div > div > section > div > div.views-element-container.form-group > div > nav > ul"
  );
  var pageNumberList = paginator.getElementsByTagName("li");
  var queryStringAndTitleList = [];
  for (pageNumber of pageNumberList) {
    var anchorTag = pageNumber.getElementsByTagName("a")[0];
    if (anchorTag) {
      // console.log([anchorTag.getAttribute('href'), anchorTag.getAttribute('title')]);
      queryStringAndTitleList.push([
        anchorTag.getAttribute("href"),
        anchorTag.getAttribute("title"),
      ]);
    }
  }
  var pageSelectorUrlQueryString = queryStringAndTitleList.find(
    ([, title]) => title === "Current page"
  )[0];
  // console.log(pageSelectorUrlQueryString);
  var pageNumber = new URLSearchParams(pageSelectorUrlQueryString).get("page");
  // console.log(pageNumber);
  return Number(pageNumber);
}

function getCellData({ row, column }) {
  // name and vid
  var downloadAnchorTag = document.querySelector(
    `body > div.dialog-off-canvas-main-canvas > div > div > section > div > div.views-element-container.form-group > div > div.view-content > div.views-view-grid.horizontal.cols-4.clearfix > div.views-row.clearfix.row-${row} > div.views-col.col-${column} > div.views-field.views-field-nothing-3 > span.field-content > a`
  );

  var stateDuringScraping = document.querySelector(
    `body > div.dialog-off-canvas-main-canvas > div > div > section > div > div.views-element-container.form-group > div > div.view-content > div.views-view-grid.horizontal.cols-4.clearfix > div.views-row.clearfix.row-${row} > div.views-col.col-${column} > span.views-field.views-field-moderation-state > span.field-content`
  ).innerText;

  var emailId = document.querySelector(
    `body > div.dialog-off-canvas-main-canvas > div > div > section > div > div.views-element-container.form-group > div > div.view-content > div.views-view-grid.horizontal.cols-4.clearfix > div.views-row.clearfix.row-${row} > div.views-col.col-${column} > span.views-field.views-field-field-email > span.field-content`
  ).innerText;

  var profession = document.querySelector(
    `body > div.dialog-off-canvas-main-canvas > div > div > section > div > div.views-element-container.form-group > div > div.view-content > div.views-view-grid.horizontal.cols-4.clearfix > div.views-row.clearfix.row-${row} > div.views-col.col-${column} > span.views-field.views-field-field-i-am > span.field-content`
  ).innerText;

  var resolution = document
    .querySelector(
      `body > div.dialog-off-canvas-main-canvas > div > div > section > div > div.views-element-container.form-group > div > div.view-content > div.views-view-grid.horizontal.cols-4.clearfix > div.views-row.clearfix.row-${row} > div.views-col.col-${column} > div.views-field.views-field-nothing-1 > span.field-content`
    )
    .innerText.trim();

  var source = document
    .querySelector(
      `body > div.dialog-off-canvas-main-canvas > div > div > section > div > div.views-element-container.form-group > div > div.view-content > div.views-view-grid.horizontal.cols-4.clearfix > div.views-row.clearfix.row-${row} > div.views-col.col-${column} > div.views-field.views-field-field-source > div`
    )
    .innerText.trim();

  var refreshAnchorTag = document.querySelector(
    `body > div.dialog-off-canvas-main-canvas > div > div > section > div > div.views-element-container.form-group > div > div.view-content > div.views-view-grid.horizontal.cols-4.clearfix > div.views-row.clearfix.row-${row} > div.views-col.col-${column} > div.views-field.views-field-nothing-2 > span > a`
  );

  var firstName = document.querySelector(
    `body > div.dialog-off-canvas-main-canvas > div > div > section > div > div.views-element-container.form-group > div > div.view-content > div.views-view-grid.horizontal.cols-4.clearfix > div.views-row.clearfix.row-${row} > div.views-col.col-${column} > span.views-field.views-field-field-first-name > span.field-content`
  ).innerText;

  var lastName = document.querySelector(
    `body > div.dialog-off-canvas-main-canvas > div > div > section > div > div.views-element-container.form-group > div > div.view-content > div.views-view-grid.horizontal.cols-4.clearfix > div.views-row.clearfix.row-${row} > div.views-col.col-${column} > div.views-field.views-field-field-last-name > div`
  ).innerText;

  return {
    row,
    column,
    index: 4 * (row - 1) + column,
    pageNumber,

    vid: downloadAnchorTag.getAttribute("vid"),
    bid: refreshAnchorTag.getAttribute("bid"),
    name: downloadAnchorTag.getAttribute("name"),
    stateDuringScraping,
    emailId,
    resolution,

    vid_of_bid: refreshAnchorTag.getAttribute("vid"),
    firstName,
    lastName,
    profession,
    source,
  };
}

function scrapeData(addHeader) {
  const pageNumber = getCurrentPageNumber() + 1;
  const dataList = [];
  for (let row = 1; row < 6; row++) {
    for (let column = 1; column < 5; column++) {
      var data = getCellData({ row, column, pageNumber });
      dataList.push(data);
    }
  }
  downloadJSON(pageNumber, dataList);
  downloadCSV(pageNumber, convertToCSV(dataList, addHeader));
  return dataList;
}

function getFetchPayload({ index, dataList }) {
  const { vid: video_id, pageNumber, name } = dataList[index];
  var payload = { video_id, name };
  console.log(index, payload, "getFetchPayload");
  return {
    headers: {
      accept: "*/*",
      "accept-language":
        "en-IN,en;q=0.9,hi-IN;q=0.8,hi;q=0.7,en-US;q=0.6,en-GB;q=0.5",
      "cache-control": "no-cache",
      "content-type": "application/json",
      newrelic:
        "eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjMwMTkyMDciLCJhcCI6IjEzODYwOTc5OTQiLCJpZCI6ImVhMTQzYjQ1OTUxNTI2OGEiLCJ0ciI6IjA3NGVhMzI3NGU4NDA1YzY0NDNjOGEyMWY1YTYyMTAwIiwidGkiOjE2OTkzOTIyNzg2NjksInRrIjoiMTQ2MDUzMiJ9fQ==",
      pragma: "no-cache",
      "sec-ch-ua":
        '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
      "sec-ch-ua-mobile": "?0",
      "sec-ch-ua-platform": '"macOS"',
      "sec-fetch-dest": "empty",
      "sec-fetch-mode": "cors",
      "sec-fetch-site": "same-origin",
      traceparent: "00-074ea3274e8405c6443c8a21f5a62100-ea143b459515268a-01",
      tracestate:
        "1460532@nr=0-1-3019207-1386097994-ea143b459515268a----1699392278669",
    },
    referrer: `https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created%5Bmin%5D%5Bdate%5D=&created%5Bmax%5D%5Bdate%5D=&page=${pageNumber}`,
    referrerPolicy: "strict-origin-when-cross-origin",
    body: JSON.stringify(payload),
    method: "POST",
    mode: "cors",
    credentials: "include",
  };
}

function counter() {
  pending -= 1;
  console.log("pending", pending);
  if (pending === 0) {
    console.log("======= Batch Finished ========");
    pending = 20;
    const nextPageIndex = getCurrentPageNumber() + 1;
    window.location.replace(
      `https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=&created[max][date]=&page=${nextPageIndex}`
    );
  }
}

async function downloadVideo(dataList) {
  for (let index = 0; index < dataList.length; index++) {
    fetch(
      "https://pledgewithpfizerco.pfizersite.io/download_video",
      getFetchPayload({ index, dataList })
    )
      .then((response) => {
        console.log(
          index,
          response.status,
          "getFetchPayload ------------>>",
          dataList[index]
        );
        return response.blob();
      })
      .then((blobData) => {
        console.log(index, "blobData");
        const {
          vid: video_id,
          name,
          pageNumber,
          row,
          column,
        } = dataList[index];
        var a = document.createElement("a");
        a.href = window.URL.createObjectURL(blobData);
        a.download = `${pageNumber}_${row}_${column}_${video_id}_${name}`;
        a.click();
        counter();
        return Promise.resolve();
      })
      .catch((error) => console.error(error));
  }
  return;
}

function boomboom() {
  var dataList = scrapeData(false);
  downloadVideo(dataList)
    .then((d) => {
      console.log(d);
    })
    .catch((e) => {
      console.error(e);
    });
}

var pending = 20;
var dataList = [];
boomboom();

// const response = await fetch(
//   "https://pledgewithpfizerco.pfizersite.io/download_video",
//   getFetchPayload({ pageNumber, payload })
// );
// console.log(index, response.status, "------------>>", data);
// const res = await response.blob();
// var a = document.createElement("a");
// a.href = window.URL.createObjectURL(res);
// a.download = `${pageNumber}_${row}_${column}_${video_id}_${name}`;
// a.click();
