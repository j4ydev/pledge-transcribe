function printAllFilesOfAFolderWithLink(
  sheet,
  childFolder,
  skipBatch = false,
  richValueBatch
) {
  var files = childFolder.getFiles();
  var rowData = [];
  var max = 1000;
  var count = 0;
  while (files.hasNext()) {
    var file = files.next();
    var url = file.getUrl();
    var fileName = file.getName();
    var vid = fileName.split("_")?.[0] || "";
    var richValueVid = SpreadsheetApp.newRichTextValue().setText(vid).build();
    var richValueFileName = SpreadsheetApp.newRichTextValue()
      .setText(fileName)
      .setLinkUrl(url)
      .build();
    var plainTextURL = SpreadsheetApp.newRichTextValue().setText(url).build();
    var data = skipBatch
      ? [richValueVid, richValueFileName, plainTextURL]
      : [richValueBatch, richValueVid, richValueFileName, plainTextURL];
    // Logger.log(fileName)
    rowData.push(data);
    if (count == max) {
      Logger.log("-----------------------");
      var lastRow = sheet.getLastRow();
      sheet
        .getRange(lastRow + 1, 1, rowData.length, rowData[0].length)
        .setRichTextValues(rowData);
      rowData = [];
      count = 0;
    } else {
      count = count + 1;
    }
  }
  var lastRow = sheet.getLastRow();
  sheet
    .getRange(lastRow + 1, 1, rowData.length, rowData[0].length)
    .setRichTextValues(rowData);
}

// function printEachFileNameFromAllFolderToDepthOne(sheet, videoBatchesFolderId) {
//   var folder = DriveApp.getFolderById(videoBatchesFolderId);
//   var childFolders = folder.getFolders();
//   while (childFolders.hasNext()) {
//     var childFolder = childFolders.next();
//     var batchNumber = childFolder.getName();
//     var batchDirURL = childFolder.getUrl();
//     // Logger.log(batchNumber);
//     // if (batchNumber != 42) continue;
//     var richValueBatch = SpreadsheetApp.newRichTextValue()
//       .setText(batchNumber)
//       .setLinkUrl(batchDirURL)
//       .build();
//     Logger.log(batchNumber, "printAllFilesOfAFolderWithLink");
//     printAllFilesOfAFolderWithLink(sheet, childFolder, false, richValueBatch);
//   }
// }

// function main_move_duplicate() {
//   var spreadsheetId = "1F_RR7YnBYSV0L-wpFHSall3a5RJ-4qT7BhXhD3I2Xes";
//   var screenShotLedgerSheetName = "t";
//   var sheet = SpreadsheetApp.openById(spreadsheetId).getSheetByName(screenShotLedgerSheetName);
//   // var values = sheet.getRange("A1:A234").getRichTextValues();
//   // var data = []
//   // Logger.log(values.length)
//   // for (var i = 0; i<values.length; i++) {
//   //   var url = values[i][0].getLinkUrl();
//   //   data.push([url]);
//   // }
//   // sheet.getRange("B1:B234").setValues(data);

//   var destination = "1M7Y7zbxKp3gWlJKz2i-tXYoxOwFPGU9-";
//   var folder = DriveApp.getFolderById(destination);
//   var values = sheet.getRange("B1:B234").getValues();
//   for (var i = 0; i<values.length; i++) {
//     var fileId = values[i][0];
//     Logger.log(fileId);
//     var file = DriveApp.getFileById(fileId);
//     file.moveTo(folder);
//   }
// }

function main() {
  // var spreadsheetId = "1F_RR7YnBYSV0L-wpFHSall3a5RJ-4qT7BhXhD3I2Xes";
  // var spreadsheetId = "1M1NLWJMRXczWg3EFJUQVf-NOP4diZiEDJ5rr0kCTkLw";
  var spreadsheetId = "1524Sglo3uKVpJ4foYv3qQTRk6su-GZNbTF-ghO4LH_c";
  var sheet;

  // var videoLedgersheetName = "sl"; // "video-ledger";
  // var videoBatcheLedgerFolderId = "1uPMVJPVjryatZmpYdNwX0SETHuEsa0xM";
  // sheet = SpreadsheetApp.openById(spreadsheetId).getSheetByName(videoLedgersheetName);
  // Logger.log(sheet.getName());
  // printEachFileNameFromAllFolderToDepthOne(sheet, videoBatcheLedgerFolderId);

  // var screenShotLedgerFolderId = "1uPMVJPVjryatZmpYdNwX0SETHuEsa0xM";
  // var screenShotLedgerSheetName = "sl";
  // sheet = SpreadsheetApp.openById(spreadsheetId).getSheetByName(screenShotLedgerSheetName);
  // printEachFileNameFromAllFolderToDepthOne(sheet, screenShotLedgerFolderId);

  // var duplicateIterationOneInputFolderId = "1OFlDPY9A04NyOBA0M33wfo2ZE-HVuVgo";
  // var duplicateIterationOneSheetName = "dup-itr-1-ip";
  // sheet = SpreadsheetApp.openById(spreadsheetId).getSheetByName(duplicateIterationOneSheetName);
  // var folder = DriveApp.getFolderById(duplicateIterationOneInputFolderId);
  // printAllFilesOfAFolderWithLink(sheet, folder, true);

  // var duplicateIterationOneInputFolderId = "1O5EqzJHHimmhTZ-zABCApIkfFfoxuHMq";
  // var duplicateIterationOneInputFolderId = "1O5EqzJHHimmhTZ-zABCApIkfFfoxuHMq"; //manual
  var duplicateIterationOneInputFolderId = "15em_Zq_KqU89TyYXoDlzOm7ZVjoOQqG8"; //automated
  var duplicateIterationOneSheetName = "a";
  sheet = SpreadsheetApp.openById(spreadsheetId).getSheetByName(
    duplicateIterationOneSheetName
  );
  var folder = DriveApp.getFolderById(duplicateIterationOneInputFolderId);
  printAllFilesOfAFolderWithLink(sheet, folder, true);
}

// -----------

// function printAllFilesOfAFolderWithLink(sheet, childFolder, skipBatch = false, richValueBatch) {
//   var files = childFolder.getFiles();
//   var rowData = [];
//   var max = 1000;
//   var count = 0;
//   while (files.hasNext()) {
//     var file = files.next();
//     var url = file.getUrl();
//     var fileName = file.getName();
//     var vid = fileName.split('_')?.[0] || '';
//     var richValueVid = SpreadsheetApp.newRichTextValue()
//       .setText(vid)
//       .build();
//     var richValueFileName = SpreadsheetApp.newRichTextValue()
//       .setText(fileName)
//       .setLinkUrl(url)
//       .build();
//     var plainTextURL = SpreadsheetApp.newRichTextValue().setText(url).build();
//     var data = skipBatch ? [richValueVid, richValueFileName, plainTextURL] : [richValueBatch, richValueVid, richValueFileName, plainTextURL];
//     // Logger.log(fileName)
//     rowData.push(data);
//     if (count == max) {
//       Logger.log("-----------------------");
//       var lastRow = sheet.getLastRow();
//       sheet.getRange(lastRow + 1, 1, rowData.length, rowData[0].length).setRichTextValues(rowData);
//       rowData = [];
//       count = 0;
//     } else {
//       count = count + 1;
//     }
//   }
//   var lastRow = sheet.getLastRow();
//   sheet.getRange(lastRow + 1, 1, rowData.length, rowData[0].length).setRichTextValues(rowData);
// }

// function main() {
// var spreadsheetId = "1524Sglo3uKVpJ4foYv3qQTRk6su-GZNbTF-ghO4LH_c";
// var sheet;
// var duplicateIterationOneInputFolderId = "15em_Zq_KqU89TyYXoDlzOm7ZVjoOQqG8"; //automated
// var duplicateIterationOneSheetName = "a";
// sheet = SpreadsheetApp.openById(spreadsheetId).getSheetByName(duplicateIterationOneSheetName);
// var folder = DriveApp.getFolderById(duplicateIterationOneInputFolderId);
// printAllFilesOfAFolderWithLink(sheet, folder, true);
// }
