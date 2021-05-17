const express = require('express')
const app = express()
const port = 3000

app.use(express.static('public'))

app.get('/hospital', function(req, res){
    var request = require('request');
    var url = 'http://apis.data.go.kr/6260000/MedicInstitService/MedicalInstitInfo?serviceKey=RgUnx4TnQgMlmue6bRaeR3br4dOxJU6bWx6vt2%2BTQtab7b%2BNABOmP9F%2F%2BqtVzzalyPCYl68xNBzpifWs7XQZiQ%3D%3D&pageNo=1&numOfRows=2370&resultType=json&instit_kind='
    url += encodeURI("의원");

    var options = {
        'method': 'GET',
        'url': url,
        'headers': {
        }
    };
    request(options, function (error, response) { 
        if (error) throw new Error(error);
        res.send(response.body);
    });
});

app.get('/korea', function(req, res){
    var request = require('request');
    var url = 'http://apis.data.go.kr/6260000/MedicInstitService/MedicalInstitInfo?serviceKey=RgUnx4TnQgMlmue6bRaeR3br4dOxJU6bWx6vt2%2BTQtab7b%2BNABOmP9F%2F%2BqtVzzalyPCYl68xNBzpifWs7XQZiQ%3D%3D&pageNo=1&numOfRows=1122&resultType=json&instit_kind='
    url += encodeURI("한의원");

    var options = {
        'method': 'GET',
        'url': url,
        'headers': {
        }
    };
    request(options, function (error, response) { 
        if (error) throw new Error(error);
        res.send(response.body);
    });
});
app.get('/dental', function(req, res){
    var request = require('request');
    var url = 'http://apis.data.go.kr/6260000/MedicInstitService/MedicalInstitInfo?serviceKey=RgUnx4TnQgMlmue6bRaeR3br4dOxJU6bWx6vt2%2BTQtab7b%2BNABOmP9F%2F%2BqtVzzalyPCYl68xNBzpifWs7XQZiQ%3D%3D&pageNo=1&numOfRows=1268&resultType=json&instit_kind='
    url += encodeURI("치과의원");

    var options = {
        'method': 'GET',
        'url': url,
        'headers': {
        }
    };
    request(options, function (error, response) { 
        if (error) throw new Error(error);
        res.send(response.body);
    });
});
app.get('/pharm', function(req, res){
    var request = require('request');
    var url = 'http://apis.data.go.kr/6260000/MedicInstitService/MedicalInstitInfo?serviceKey=RgUnx4TnQgMlmue6bRaeR3br4dOxJU6bWx6vt2%2BTQtab7b%2BNABOmP9F%2F%2BqtVzzalyPCYl68xNBzpifWs7XQZiQ%3D%3D&pageNo=1&numOfRows=1579&resultType=json&instit_kind='
    url += encodeURI("약국");

    var options = {
        'method': 'GET',
        'url': url,
        'headers': {
        }
    };
    request(options, function (error, response) { 
        if (error) throw new Error(error);
        res.send(response.body);
    });
});
app.listen(port, () => console.log(`Example app listening at http://localhost:${port}`))