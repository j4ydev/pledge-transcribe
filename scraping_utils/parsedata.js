/*
Next Steps
1. capture nid - done
2. capture bid - done
3. capture URL to accept video
4. capture URL to reject video
5. define the batch index - document the date range for batch index - so that a batch once scrapped need not be repeated, and avoid video duplicates
6. since the oldest is last - update flow to parse in reverse
7. file name format: bid_vid_file-name-suffix.mp4
8. Align the CSV with google spreadsheet column sequence
*/

const batch = {
  1: {
    min_date: "2023-08-01",
    max_date: "2023-08-31",
    pageCount: 3,
    videoCount: 52,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2023-08-01&created[max][date]=2023-08-31&page=0",
  },
  2: {
    min_date: "2023-09-01",
    max_date: "2023-09-10",
    pageCount: 19,
    videoCount: 367,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2023-09-01&created[max][date]=2023-09-10&page=0",
  },
  3: {
    min_date: "2023-09-11",
    max_date: "2023-09-20",
    pageCount: 32,
    videoCount: 634,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2023-09-11&created[max][date]=2023-09-20&page=0",
  },
  4: {
    min_date: "2023-09-21",
    max_date: "2023-09-30",
    pageCount: 15,
    videoCount: 283,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2023-09-21&created[max][date]=2023-09-30&page=0",
  },
  5: {
    min_date: "2023-10-01",
    max_date: "2023-10-15",
    pageCount: 17,
    videoCount: 328,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2023-10-01&created[max][date]=2023-10-15&page=0",
  },
  6: {
    min_date: "2023-10-16",
    max_date: "2023-10-21",
    pageCount: 34,
    videoCount: 675,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2023-10-16&created[max][date]=2023-10-21&page=0",
  },
  7: {
    min_date: "2023-10-22",
    max_date: "2023-10-25",
    pageCount: 36,
    videoCount: 710,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2023-10-22&created[max][date]=2023-10-25&page=0",
  },
  8: {
    min_date: "2023-10-26",
    max_date: "2023-10-28",
    pageCount: 41,
    videoCount: 810,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2023-10-26&created[max][date]=2023-10-28&page=0",
  },
  9: {
    min_date: "2023-10-29",
    max_date: "2023-10-31",
    pageCount: 20,
    videoCount: 400,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2023-10-29&created[max][date]=2023-10-31&page=0",
  },
  10: {
    min_date: "2023-11-01",
    max_date: "2023-11-05",
    pageCount: 20,
    videoCount: 397,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2023-11-01&created[max][date]=2023-11-05&page=0",
  },
  11: {
    min_date: "2023-11-06",
    max_date: "2023-11-12",
    pageCount: 30,
    videoCount: 594,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2023-11-06&created[max][date]=2023-11-12&page=0",
  },
  12: {
    min_date: "2023-11-13",
    max_date: "2023-11-20",
    pageCount: 26,
    videoCount: 503,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2023-11-13&created[max][date]=2023-11-20&page=0",
  },
  13: {
    min_date: "2023-11-21",
    max_date: "2023-11-22",
    pageCount: 21,
    videoCount: 402,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2023-11-21&created[max][date]=2023-11-22&page=0",
  },
  14: {
    min_date: "2023-11-23",
    max_date: "2023-11-24",
    pageCount: 21,
    videoCount: 406,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2023-11-23&created[max][date]=2023-11-24&page=0",
  },
  15: {
    min_date: "2023-11-25",
    max_date: "2023-11-27",
    pageCount: 17,
    videoCount: 337,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2023-11-25&created[max][date]=2023-11-27&page=0",
  },
  16: {
    min_date: "2023-11-28",
    max_date: "2023-11-30",
    pageCount: 11,
    videoCount: 218,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2023-11-28&created[max][date]=2023-11-30&page=0",
  },
  17: {
    min_date: "2023-12-01",
    max_date: "2023-12-14",
    pageCount: 19,
    videoCount: 369,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2023-12-01&created[max][date]=2023-12-14&page=0",
  },
  18: {
    min_date: "2023-12-15",
    max_date: "2023-12-18",
    pageCount: 20,
    videoCount: 400,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2023-12-15&created[max][date]=2023-12-18&page=0",
  },
  19: {
    min_date: "2023-12-19",
    max_date: "2023-12-25",
    pageCount: 11,
    videoCount: 212,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2023-12-19&created[max][date]=2023-12-25&page=0",
  },
  20: {
    min_date: "2023-12-26",
    max_date: "2023-12-26",
    pageCount: 18,
    videoCount: 359,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2023-12-19&created[max][date]=2023-12-25&page=0",
  },
  21: {
    min_date: "2023-12-27",
    max_date: "2023-12-27",
    pageCount: 15,
    videoCount: 299,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2023-12-19&created[max][date]=2023-12-25&page=0",
  },
  22: {
    min_date: "2023-12-28",
    max_date: "2023-12-30",
    pageCount: 15,
    videoCount: 296,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2023-12-28&created[max][date]=2023-12-30&page=0",
  },
  23: {
    min_date: "2023-12-31",
    max_date: "2023-12-31",
    pageCount: 41,
    videoCount: 810,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2023-12-31&created[max][date]=2023-12-31&page=0",
  },
  24: {
    min_date: "2024-01-01",
    max_date: "2024-01-01",
    pageCount: 30,
    videoCount: 583,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2024-01-01&created[max][date]=2024-01-01&page=0",
  },
  25: {
    min_date: "2024-01-02",
    max_date: "2024-01-02",
    pageCount: 53,
    videoCount: 1042,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2024-01-02&created[max][date]=2024-01-02&page=0",
  },
  26: {
    min_date: "2024-01-03",
    max_date: "2024-01-03",
    pageCount: 17,
    videoCount: 340,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2024-01-03&created[max][date]=2024-01-03&page=0",
  },
  27: {
    min_date: "2024-01-04",
    max_date: "2024-01-07",
    pageCount: 11,
    videoCount: 208,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2024-01-04&created[max][date]=2024-01-07&page=0",
  },
  28: {
    min_date: "2024-01-08",
    max_date: "2024-01-16",
    pageCount: 11,
    videoCount: 208,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2024-01-08&created[max][date]=2024-01-16&page=0",
  },
  29: {
    min_date: "2024-01-17",
    max_date: "2024-01-19",
    pageCount: 15,
    videoCount: 295,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2024-01-17&created[max][date]=2024-01-19&page=0",
  },
  30: {
    min_date: "2024-01-20",
    max_date: "2024-01-29",
    pageCount: 14,
    videoCount: 275,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2024-01-20&created[max][date]=2024-01-29&page=0",
  },
  31: {
    min_date: "2024-01-30",
    max_date: "2024-02-02",
    pageCount: 17,
    videoCount: 322,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2024-01-30&created[max][date]=2024-02-02&page=0",
  },
  32: {
    min_date: "2024-02-03",
    max_date: "2024-02-03",
    pageCount: 56,
    videoCount: 1106,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2024-02-03&created[max][date]=2024-02-03&page=0",
  },
  33: {
    min_date: "2024-02-04",
    max_date: "2024-02-04",
    pageCount: 66,
    videoCount: 1306,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2024-02-04&created[max][date]=2024-02-04&page=0",
  },
  34: {
    min_date: "2024-02-05",
    max_date: "2024-02-05",
    pageCount: 29,
    videoCount: 569,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2024-02-05&created[max][date]=2024-02-05&page=0",
  },
  35: {
    min_date: "2024-02-06",
    max_date: "2024-02-07",
    pageCount: 21,
    videoCount: 411,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2024-02-06&created[max][date]=2024-02-07&page=0",
  },
  36: {
    min_date: "2024-02-08",
    max_date: "2024-02-09",
    pageCount: 17,
    videoCount: 324,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2024-02-08&created[max][date]=2024-02-09&page=0",
  },
  37: {
    min_date: "2024-02-10",
    max_date: "2024-02-11",
    pageCount: 8,
    videoCount: 148,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2024-02-10&created[max][date]=2024-02-11&page=0",
  },
  38: {
    min_date: "2024-02-12",
    max_date: "2024-02-15",
    pageCount: 27,
    videoCount: 524,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2024-02-12&created[max][date]=2024-02-15&page=0",
  },
  39: {
    min_date: "2024-02-16",
    max_date: "2024-02-17",
    pageCount: 28,
    videoCount: 548,
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=All&title=&created[min][date]=2024-02-16&created[max][date]=2024-02-17&page=0",
  },
  100: {
    min_date: "2022-01-01",
    max_date: "2024-02-11",
    pageCount: 6,
    videoCount: 103,
    moderationState: "pfizer_workflow-draft",
    pageZeroURL:
      "https://pledgewithpfizerco.pfizersite.io/amr-video?moderation_state=pfizer_workflow-draft&title=&created[min][date]=2023-01-01&created[max][date]=2024-02-11",
  },
};

const baseURL = "https://pledgewithpfizerco.pfizersite.io/amr-video";
const getBatchUrlQueryString = ({ batchNumber = "1", pageNumber = 0 }) => {
  const minDate = batch[batchNumber].min_date || "";
  const maxDate = batch[batchNumber].max_date || "";
  const moderationState = batch[batchNumber].moderationState || "All";
  return `moderation_state=${moderationState}&title=&created[min][date]=${minDate}&created[max][date]=${maxDate}&page=${pageNumber}`;
};
const getBatchUrl = ({ batchNumber = "1", pageNumber = 0 }) =>
  `${baseURL}?${getBatchUrlQueryString({ batchNumber, pageNumber })}`;

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
function downloadCSV(pageNumber, csv, batchNumber = "1") {
  var blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
  var a = document.createElement("a");
  a.href = window.URL.createObjectURL(blob);
  a.download = `${batchNumber}_${pageNumber}.csv`;
  a.click();
}
function downloadJSON({ pageNumber, dataList, batchNumber = "1" }) {
  const blob = new Blob([JSON.stringify(dataList)], { type: "text/json" });
  var a = document.createElement("a");
  a.href = window.URL.createObjectURL(blob);
  a.download = `${batchNumber}_${pageNumber}.json`;
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

function getCellData({ row, column, pageNumber, batchNumber }) {
  // name and vid
  var downloadAnchorTag = document.querySelector(
    `body > div.dialog-off-canvas-main-canvas > div > div > section > div > div.views-element-container.form-group > div > div.view-content > div.views-view-grid.horizontal.cols-4.clearfix > div.views-row.clearfix.row-${row} > div.views-col.col-${column} > div.views-field.views-field-nothing-3 > span.field-content > a`
  );

  var stateDuringScraping =
    document.querySelector(
      `body > div.dialog-off-canvas-main-canvas > div > div > section > div > div.views-element-container.form-group > div > div.view-content > div.views-view-grid.horizontal.cols-4.clearfix > div.views-row.clearfix.row-${row} > div.views-col.col-${column} > span.views-field.views-field-moderation-state > span.field-content`
    )?.innerText || "";

  var emailId =
    document.querySelector(
      `body > div.dialog-off-canvas-main-canvas > div > div > section > div > div.views-element-container.form-group > div > div.view-content > div.views-view-grid.horizontal.cols-4.clearfix > div.views-row.clearfix.row-${row} > div.views-col.col-${column} > span.views-field.views-field-field-email > span.field-content`
    )?.innerText || "";

  var profession =
    document.querySelector(
      `body > div.dialog-off-canvas-main-canvas > div > div > section > div > div.views-element-container.form-group > div > div.view-content > div.views-view-grid.horizontal.cols-4.clearfix > div.views-row.clearfix.row-${row} > div.views-col.col-${column} > span.views-field.views-field-field-i-am > span.field-content`
    )?.innerText || "";

  var resolution =
    document
      .querySelector(
        `body > div.dialog-off-canvas-main-canvas > div > div > section > div > div.views-element-container.form-group > div > div.view-content > div.views-view-grid.horizontal.cols-4.clearfix > div.views-row.clearfix.row-${row} > div.views-col.col-${column} > div.views-field.views-field-nothing-1 > span.field-content`
      )
      ?.innerText.trim() || "";

  var source =
    document
      .querySelector(
        `body > div.dialog-off-canvas-main-canvas > div > div > section > div > div.views-element-container.form-group > div > div.view-content > div.views-view-grid.horizontal.cols-4.clearfix > div.views-row.clearfix.row-${row} > div.views-col.col-${column} > div.views-field.views-field-field-source > div`
      )
      ?.innerText.trim() || "";

  var refreshAnchorTag = document.querySelector(
    `body > div.dialog-off-canvas-main-canvas > div > div > section > div > div.views-element-container.form-group > div > div.view-content > div.views-view-grid.horizontal.cols-4.clearfix > div.views-row.clearfix.row-${row} > div.views-col.col-${column} > div.views-field.views-field-nothing-2 > span > a`
  );

  var firstName =
    document.querySelector(
      `body > div.dialog-off-canvas-main-canvas > div > div > section > div > div.views-element-container.form-group > div > div.view-content > div.views-view-grid.horizontal.cols-4.clearfix > div.views-row.clearfix.row-${row} > div.views-col.col-${column} > span.views-field.views-field-field-first-name > span.field-content`
    )?.innerText || "";

  var lastName =
    document.querySelector(
      `body > div.dialog-off-canvas-main-canvas > div > div > section > div > div.views-element-container.form-group > div > div.view-content > div.views-view-grid.horizontal.cols-4.clearfix > div.views-row.clearfix.row-${row} > div.views-col.col-${column} > div.views-field.views-field-field-last-name > div`
    )?.innerText || "";

  var nid =
    document
      .querySelector(
        `body > div.dialog-off-canvas-main-canvas > div > div > section > div > div.views-element-container.form-group > div > div.view-content > div.views-view-grid.horizontal.cols-4.clearfix > div.views-row.clearfix.row-${row} > div.views-col.col-${column} > span.views-field.views-field-nothing > span > div > a`
      )
      ?.getAttribute("nid") || "";

  var buttonTag1 = document.querySelector(
    `body > div.dialog-off-canvas-main-canvas > div > div > section > div > div.views-element-container.form-group > div > div.view-content > div.views-view-grid.horizontal.cols-4.clearfix > div.views-row.clearfix.row-${row} > div.views-col.col-${column} > span.views-field.views-field-set-moderation-state > span > ul > li:nth-child(1) > a`
  );
  var buttonTag2 = document.querySelector(
    `body > div.dialog-off-canvas-main-canvas > div > div > section > div > div.views-element-container.form-group > div > div.view-content > div.views-view-grid.horizontal.cols-4.clearfix > div.views-row.clearfix.row-${row} > div.views-col.col-${column} > span.views-field.views-field-set-moderation-state > span > ul > li:nth-child(2) > a`
  );
  var links = {};
  if (buttonTag1) {
    links[buttonTag1.innerText] = decodeURIComponent(
      decodeURIComponent(buttonTag1.getAttribute("href") || "").split("?")[0]
    );
  }
  if (buttonTag2) {
    links[buttonTag2.innerText] = decodeURIComponent(
      decodeURIComponent(buttonTag2.getAttribute("href") || "").split("?")[0]
    );
  }

  const name = downloadAnchorTag?.getAttribute("name") || "";
  const bid = refreshAnchorTag?.getAttribute("bid") || "";
  const vid = downloadAnchorTag?.getAttribute("vid") || "";
  const filenameSuffix = name
    .replace(/[^a-zA-Z0-9-_.]/g, "_")
    .replaceAll("__", "_")
    .replaceAll("__", "_")
    .replaceAll("__", "_")
    .replaceAll("__", "_")
    .toLowerCase();
  const fileName = vid ? `${vid}_${filenameSuffix}.mp4` : "";

  return vid
    ? {
        vid,
        name,
        stateDuringScraping,
        emailId,
        resolution,
        fileName,

        firstName,
        lastName,
        profession,

        vid_of_bid: refreshAnchorTag?.getAttribute("vid"),
        bid,
        nid,
        batchNumber,
        pageNumber,
        row,
        column,
        index: 4 * (row - 1) + column,
        publish: links["Set to Published"],
        reject: links["Set to Reject"],
        draft: links["Set to Draft"],
        source,
      }
    : {};
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
    referrer: `${baseURL}?moderation_state=All&title=&created[min][date]=&created[max][date]=&page=${pageNumber}`,
    referrerPolicy: "strict-origin-when-cross-origin",
    body: JSON.stringify(payload),
    method: "POST",
    mode: "cors",
    credentials: "include",
  };
}

function counter(batchNumber) {
  pending -= 1;
  console.log("pending", pending);
  if (pending === 0) {
    console.log("======= PAGE Finished ========");
    pending = 20;
    const nextPageIndex = getCurrentPageNumber() + 1;
    if (Number.parseInt(batch[batchNumber].pageCount) >= nextPageIndex) {
      window.location.replace(
        `${getBatchUrl({ batchNumber, pageNumber: nextPageIndex })}`
      );
    } else {
      console.log("===XX==+ Batch Finished ===XX===");
      window.location.replace("https://google.com");
    }
  }
}

function scrapeData({ addHeader, batchNumber = "1" }) {
  const pageNumber = getCurrentPageNumber() + 1;
  const dataList = [];
  for (let row = 1; row < 6; row++) {
    for (let column = 1; column < 5; column++) {
      var data = getCellData({ row, column, pageNumber, batchNumber });
      dataList.push(data);
      if (!downloadVideoFlag) {
        counter(batchNumber);
      }
    }
  }
  downloadJSON({ pageNumber, dataList, batchNumber });
  downloadCSV(pageNumber, convertToCSV(dataList, addHeader), batchNumber);
  return dataList;
}

async function downloadVideo(dataList) {
  for (let index = 0; index < dataList.length; index++) {
    if (!dataList[index].vid) continue;
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
        const { fileName } = dataList[index];

        var a = document.createElement("a");
        a.href = window.URL.createObjectURL(blobData);
        a.download = fileName;
        a.click();
        counter(batchNumber);
        return Promise.resolve();
      })
      .catch((error) => console.error(error));
  }
  return;
}

function boomboom(batchNumber) {
  var dataList = scrapeData({ addHeader, batchNumber });
  if (downloadVideoFlag) {
    downloadVideo(dataList)
      .then((d) => {
        console.log(d);
      })
      .catch((e) => {
        console.error(e);
      });
  }
}

const addHeader = false;
const downloadVideoFlag = true;
const batchNumber = "37";
var pending = 20;
var dataList = [];
boomboom(batchNumber);

/*
var arr = [];
var urlSuffix = "?destination=/amr-video?moderation_state=All&title=&created[min][date]=2023-10-22&created[max][date]=2023-10-25&page=0";
for (let index = 0; index < arr.length; index++) {
  const url = `${arr[index]}${urlSuffix}`;
  fetch(url).then((response) => { console.log(index, response.status, url); return response.blob();}).then(x => x).catch(error => console.error(error));
}
*/
