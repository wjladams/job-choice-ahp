/**
* Helper functions for the results.html.
* This is here to make that file a bit easier to read.
*/

function twoDArray(nrows, ncols) {
  let rval = []
  for(let r=0; r < nrows; r++) {
    let row=[]
    for (let c=0; c < ncols; c++) {
      row.push("")
    }
    rval.push(row)
  }
  return rval
}

function gsToMatrix(spreadsheetdata) {
  let entries = spreadsheetdata["feed"]["entry"]
  let maxRow=0
  let maxCol=0
  let row=null
  let col=null
  for (let entry of entries) {
    let data = entry["gs$cell"]
    row = data["row"]
    col = data["col"]
    if (row > maxRow) {
      maxRow = row
    }
    if (col > maxCol) {
      maxCol = col
    }
  }
  let rval = twoDArray(maxRow+1, maxCol+1)
  for (let entry of entries) {
    let data = entry["gs$cell"]
    row = Number(data["row"])-1
    col = Number(data["col"])-1
    let val = data["$t"]
    if (rval[row]!=null) {
      rval[row][col]=val
    } else {
      console.log("Unknown row "+row)
    }
  }
  //Remove empty rows
  let nRval = []
  for (let row of rval) {
    let empty = true
    for (let val of row) {
      if ((val != null) && (val != "")) {
        empty = false
        break
      }
    }
    if (!empty) {
      nRval.push(row)
    }
  }
  return nRval
}
