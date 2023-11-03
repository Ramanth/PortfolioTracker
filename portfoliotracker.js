const fs = require('fs');

function evaluate_pl(column, symbol) {
    const notesData = fs.readFileSync("notes/portfolio.json", 'utf8');
    notesJson = JSON.parse(notesData);
    symbolInfo = notesJson[0][column].find(x => x.symbol == symbol)

    investedPercent = Number(symbolInfo.invested.split(" ")[0].replace("%", ""))
    investedPrice = Number(symbolInfo.cmp.split(" ")[1])
    investedAmt = 10000 * investedPercent / 100
    investedShares = investedAmt / investedPrice

    const currentPricesData = fs.readFileSync("prices.json", 'utf8');
    currPricesJson = JSON.parse(currentPricesData);

    currPrice = currPricesJson[symbol]

    pl_per_share = currPrice - investedPrice
    total_pl = pl_per_share * investedShares

    return {pl_per_share:pl_per_share, total_pl:total_pl}
}

function evaluate_pl_for_column(column) {
    let total_pl = 0
    const notesData = fs.readFileSync("notes/portfolio.json", 'utf8');
    notesJson = JSON.parse(notesData);
    columnArray = notesJson[0][column]
    for (let i = 0; i < columnArray.length; i++) {
        pl_data = evaluate_pl(column, columnArray[i].symbol)
        total_pl = total_pl + pl_data.total_pl
    }
    return parseFloat(total_pl.toFixed(2));
}

module.exports = {evaluate_pl,evaluate_pl_for_column}
