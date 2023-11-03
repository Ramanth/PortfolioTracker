const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const cors = require('cors');
const path = require('path');
const {evaluate_pl,evaluate_pl_for_column} = require('./portfoliotracker');
const moment = require('moment-timezone');
const readline = require('readline');



const app = express();
const port = 3000; // You can change this port number if needed

// Enable CORS for all routes
app.use(cors());
app.use(bodyParser.json());
// Middleware to parse JSON in the request body
app.use(express.json());

// Read stock price data from the JSON file
const rawdata = fs.readFileSync('prices.json');
const stockPrices = JSON.parse(rawdata);

const stylerawdata = fs.readFileSync('styles/stockstyles.json');
const stockData = JSON.parse(stylerawdata);

// Define a route that returns the stock price for a given stock name
app.get('/stock/price/:stockName', (req, res) => {
  const stockName = req.params.stockName.toUpperCase();
  // Check if the stockName is in the mock data
  if (stockName in stockPrices) {
    const price = stockPrices[stockName];
    const selectedStockData = stockData[stockName];
    response = {
      price: price,
      data: selectedStockData
    }
    res.send(response); // Send the stock price as a string
  } else {
    res.status(404).send('Stock not found');
  }
});



// POST endpoint to append the string to a log file
app.post('/stock/log', (req, res) => {
  const logMessage = req.body.message;

  if (!logMessage) {
    return res.status(400).json({ error: 'Message is required' });
  }

  const istTime = moment().tz('Asia/Kolkata').format('YYYY-MM-DD HH:mm:ss');

  // Create the log entry with IST timestamp
  const logEntry = `${istTime} - ${logMessage}\n`;

  // Append the log entry to the log file
  fs.appendFile('log.txt', logEntry, (err) => {
    if (err) {
      console.error('Error writing to log file:', err);
      return res.status(500).json({ error: 'Internal Server Error' });
    }
    console.log('Log entry appended to log.txt:', logEntry);

    res.status(200).json({ message: 'Log entry added successfully' });
  });
});

app.post('/stocks/redgreen', (req, res) => {
  try {
    const newNote = req.body;
    // const notes = loadNotes();
    const notes = []
    notes.push(newNote);
    saveJsonData(notes, 'redgreen');
    res.status(201).json({ message: 'Note added successfully' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Server error' });
  }
});

// Endpoint to retrieve all notes
app.get('/sample', (req, res) => {
  try {
    const notes = {
      success:"success",
      message: "message",
      statuscode: "200",
      pwdata : { 
        result : [
        {
          issuccessful : true,
          clorderid : "123456",
          error : "",
          inputparameters : {
            symbol:"TSLA",
            side:"1",
            orderQty:"10",
            price:"450",
            orderType:"1",
            userDefinedFields:{}
          },
          clOrdId: "11234"
        }
      ]}
    }
    res.status(200).json(notes);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Server error' });
  }
});

// Endpoint to retrieve all notes
app.get('/stocks/redgreen', (req, res) => {
  try {
    const notes = loadJsonData('redgreen');
    res.status(200).json(notes);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Server error' });
  }
});


app.post('/stocks/portfolio', (req, res) => {
  try {
    const newNote = req.body;
    // const notes = loadNotes();
    const notes = []
    notes.push(newNote);
    saveJsonData(notes, 'portfolio');
    res.status(201).json({ message: 'Note added successfully' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Server error' });
  }
});

// Endpoint to retrieve all notes
app.get('/stocks/portfolio', (req, res) => {
  try {
    const notes = loadJsonData('portfolio');
    res.status(200).json(notes);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Server error' });
  }
});



app.get('/stock/redgreen', (req, res) => {
  res.sendFile(path.join(__dirname, 'greenred.html'));
});

app.get('/stock/portfolio', (req, res) => {
  res.sendFile(path.join(__dirname, 'portfolio.html'));
});


app.get('/stock/portfolio/pl/:stockName', (req, res) => {
  const stockName = req.params.stockName.toUpperCase();
  result = evaluate_pl('column2', stockName)
  res.status(200).json(result);
  
});

app.get('/stock/portfolio/pl/column/:columnName', (req, res) => {
  const columnName = req.params.columnName;
  result = evaluate_pl_for_column(columnName)
  res.status(200).json(result);
});


app.get('/test', (req, res) => {
  res.sendFile(path.join(__dirname, 'test.html'));
});



// supporting functions
function getFileName(type){
  if (type == "redgreen")
    return 'notes/stock_redgreen_notes.json'
    if (type == "portfolio")
    return 'notes/portfolio.json'
}

function loadJsonData(type) {
  notesName = getFileName(type)
  try {
    const notesData = fs.readFileSync(notesName, 'utf8');
    return JSON.parse(notesData);
  } catch (error) {
    return [];
  }
}

function saveJsonData(notes, type) {
  const notesJSON = JSON.stringify(notes, null, 2);
  fs.writeFileSync(getFileName(type), notesJSON);
}

function readLinesFromFile(filePath, callback) {
  const fileStream = fs.createReadStream(filePath);
  const rl = readline.createInterface({
    input: fileStream,
    crlfDelay: Infinity
  });

  const lines = [];

  rl.on('line', (line) => {
    lines.push(line);
  });

  rl.on('close', () => {
    callback(null, lines);
  });

  rl.on('error', (error) => {
    callback(error, null);
  });
}



// Endpoint to retrieve all notes
app.get('/stock/popup/:stockName', (req, res) => {
  try {
    const stockName = req.params.stockName.toUpperCase();
    readLinesFromFile('popup\\' + stockName, (error, lines) => {
      if (error) {
        res.status(500).json({ error: 'Server error' });
      } else {
        res.status(200).send(lines);
      }
    });


    // const stockName = req.params.stockName.toUpperCase();
    // const notesData = fs.readFileSync('popup\\' + stockName, 'utf8');
    // const notes = JSON.parse(notesData);
    // res.status(200).send(notes);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Server error' });
  }
});

app.get('/stock/portfolio/popup/:stockName', (req, res) => {
  try {
    const stockName = req.params.stockName.toUpperCase();
    const notesData = fs.readFileSync('popup_portfolio\\' + stockName, 'utf8');
    // const notes = JSON.parse(notesData);
    res.status(200).send(notesData);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Server error' });
  }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
