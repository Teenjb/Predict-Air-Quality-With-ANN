const express = require('express');
const dotenv = require('dotenv');
const fs = require('fs');
const bodyParser = require('body-parser');
const { Storage } = require('@google-cloud/storage');
const moment = require('moment');

dotenv.config();

const app = express();
const port = process.env.PORT;

const storage = new Storage({
  projectId: 'YOUR_PROJECT_ID',
  credentials: {
    client_email: process.env.GCS_CLIENT_EMAIL,
    private_key: process.env.GCS_PRIVATE_KEY.replace(/\\n/g, '\n')
  }
});

// Use body-parser middleware
app.use(bodyParser.json({limit: '50mb'}));
app.use(bodyParser.urlencoded({limit: '50mb', extended: true}));

app.get('/', (req, res) => {
  res.send('Server is up');
});

app.post('/img', (req, res) => {
  let base64Image = req.body.img;
  let decodedImage = Buffer.from(base64Image, 'base64');
  const date = new Date();
  const options = { timeZone: 'Asia/Jakarta' };
  const dateInGMT7 = date.toLocaleString('en-US', options);
  const formattedDate = moment(dateInGMT7).format('YYYYMMDD_HHmmss');
  let filename = formattedDate + '.jpg';

  // Create a new blob in the bucket and upload the file data
  const blob = storage.bucket(process.env.GCS_BUCKET_NAME).file(filename);
  const blobStream = blob.createWriteStream({
    metadata: {
      contentType: 'image/jpeg',
    },
  });

  blobStream.on('error', (err) => {
    console.log(err);
    res.status(500).send('Error occurred while uploading image');
  });

  blobStream.on('finish', () => {
    // The public URL can be used to directly access the file via HTTP.
    const publicUrl = `https://storage.googleapis.com/${process.env.GCS_BUCKET_NAME}/${blob.name}`;
    res.status(200).send({imageUrl: publicUrl});
  });

  blobStream.end(decodedImage);
});

app.listen(port, '0.0.0.0', () => {
  console.log(`Server is running at http://0.0.0.0:${port}`);
});