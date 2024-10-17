
import BarChart from "./components/BarChart";

import "./App.css";
import Dropdown from "./components/Dropdown";

import { COLUMNS } from "./components/columns";

import { useState } from "react";
import { Line } from "react-chartjs-2";

import GridTiles from "./components/GridTiles";
import Map from "./components/LeafMap";
import React from "react";
import MapPolygon from "./components/LeafMapPolygon";

import { Pagination } from "./components/Pagination";
import StreamTweets from './components/StreamTweets';
import headerLogo from './Melbourne_Liveability_Index.png'


const App = () => {
  const [toggleState, setToggleState] = useState(1);

  const [twitterData, setTwitterData] = useState([]);
  const [isLoading, setIsLoading] = React.useState(true);

  const [lineData, setLineDataJson] = useState([]);
  const [lineDataFinal, setLineDataFinalJson] = useState([]);
  const [lineIsLoading, setLineIsLoading] = React.useState(true);

  const [postLineData, setPostLineDataJson] = useState([]);
  const [postLineDataFinal, setPostLineDataFinalJson] = useState([]);
  const [postIsLoading, setPostIsLoading] = React.useState(true);

  const [tableIsLoading, setTableIsLoading] = React.useState(true);
  const [EntData, setEntData] = React.useState([]);

  var entconfig = {
    method: "get",
    url:
      process.env.REACT_APP_URL +
      "/liveability/_design/liveability/_view/liveabilityView",
    headers: {
      Authorization: process.env.REACT_APP_USER,
    },
  };
  React.useEffect(() => {
    var axios = require("axios");
    axios(entconfig)
      .then((response) => {
        setEntData(response.data.rows);
      })
      .catch((error) => console.log(error));
  });

  React.useEffect(() => {
    if (EntData.length !== 0) {
      setTableIsLoading(false);
    }
  }, [EntData]);

  const [selected, setSelected] = useState("");
  const toggleTab = (index) => {
    setToggleState(index);
  };

  var lineDataPara;

  var twitterConfig = {
    method: "get",
    url: process.env.REACT_APP_URL_FLASK + "/GetSentiment",
  };

  var RAIConfig = {
    method: "get",
    url: process.env.REACT_APP_URL_FLASK + "/GetRAI",
  };

  var RAI_Postcode_Config = {
    method: "get",
    url:
      process.env.REACT_APP_URL +
      "/housing_rent_aff/_design/getLatestRAI/_view/getRAI",
    headers: {
      Authorization: process.env.REACT_APP_USER,
    },
  };

  React.useEffect(() => {
    var axios = require("axios");
    axios(twitterConfig)
      .then((response) => {
        setTwitterData(response.data);
      })
      .catch((error) => console.log(error));

    axios(RAIConfig)
      .then((response) => {
        setLineDataJson(response.data);
      })
      .catch((error) => console.log(error));
  }, []);

  React.useEffect(() => {
    var axios = require("axios");
    if (selected !== "") {
      RAI_Postcode_Config["url"] =
        RAI_Postcode_Config["url"] + '?key="' + selected + '"';

      axios(RAI_Postcode_Config)
        .then((response) => {
          setPostLineDataJson(response.data);
        })
        .catch((error) => console.log(error));
    }
  }, [selected]);

  React.useEffect(() => {
    if (twitterData.length !== 0) {
      setIsLoading(false);
    }
  }, [twitterData]);

  React.useEffect(() => {
    if (lineData.length !== 0) {
      lineDataPara = {
        labels: [
          "Q1 (2018)",
          "Q2 (2018)",
          "Q3 (2018)",
          "Q4 (2018)",
          "Q1 (2019)",
          "Q2 (2019)",
          "Q3 (2019)",
          "Q4 (2019)",
          "Q1 (2020)",
          "Q2 (2020)",
          "Q3 (2020)",
          "Q4 (2020)",
          "Q1 (2021)",
          "Q2 (2021)",
        ],
        datasets: [
          {
            label: "Rent Affordability",
            data: [
              lineData["2018Q1"],
              lineData["2018Q2"],
              lineData["2018Q3"],
              lineData["2018Q4"],
              lineData["2019Q1"],
              lineData["2019Q2"],
              lineData["2019Q3"],
              lineData["2019Q4"],
              lineData["2020Q1"],
              lineData["2020Q2"],
              lineData["2020Q3"],
              lineData["2020Q4"],
              lineData["2021Q1"],
              lineData["2021Q2"],
            ],
            fill: false,
            borderColor: "rgba(54, 162, 235, 1)",
          },
        ],
      };
      setLineDataFinalJson(lineDataPara);
      setLineIsLoading(false);
    }
  }, [lineData]);

  React.useEffect(() => {
    if (postLineData.length !== 0) {
      lineDataPara = {
        labels: [
          "Q1 (2018)",
          "Q2 (2018)",
          "Q3 (2018)",
          "Q4 (2018)",
          "Q1 (2019)",
          "Q2 (2019)",
          "Q3 (2019)",
          "Q4 (2019)",
          "Q1 (2020)",
          "Q2 (2020)",
          "Q3 (2020)",
          "Q4 (2020)",
          "Q1 (2021)",
          "Q2 (2021)",
        ],
        datasets: [
          {
            label: "Rent Affordability",
            data: [
              postLineData.rows[0].value["2018Q1"],
              postLineData.rows[0].value["2018Q2"],
              postLineData.rows[0].value["2018Q3"],
              postLineData.rows[0].value["2018Q4"],
              postLineData.rows[0].value["2019Q1"],
              postLineData.rows[0].value["2019Q2"],
              postLineData.rows[0].value["2019Q3"],
              postLineData.rows[0].value["2019Q4"],
              postLineData.rows[0].value["2020Q1"],
              postLineData.rows[0].value["2020Q2"],
              postLineData.rows[0].value["2020Q3"],
              postLineData.rows[0].value["2020Q4"],
              postLineData.rows[0].value["2021Q1"],
              postLineData.rows[0].value["2021Q2"],
            ],
            fill: false,
            borderColor: "rgba(54, 162, 235, 1)",
          },
        ],
      };
      setPostLineDataFinalJson(lineDataPara);
      setPostIsLoading(false);
    }
  }, [postLineData]);

  return (
    <div>
      <div className="heading" style={{ display:"flex" ,   flexDirection:"row"}}>
        <img src={headerLogo} alt="logo" width="100vw" height="100vw" />
        <h1 style={{marginTop:"auto",marginBottom:"auto"}}>&nbsp;&nbsp;Melbourne Liveability Index</h1>
        </div>
    
    <div className='mainContainer'>
      <div className="container">
      
        <div className="bloc-tabs">
          <button
            className={toggleState === 1 ? "tabs active-tabs" : "tabs"}
            onClick={() => toggleTab(1)}
          >
            <h3>Summary</h3>
          </button>
          <button
            className={toggleState === 2 ? "tabs active-tabs" : "tabs"}
            onClick={() => toggleTab(2)}
          >
            <h3>Postcode wise Summary</h3>
          </button>
        </div>

        <div className="content-tabs">
          <div
            className={
              toggleState === 1 ? "content  active-content" : "content"
            }
          >
            <h1>Housing</h1>
            <br></br>
            {isLoading ? (
              <h1>Loading...</h1>
            ) : (
               <GridTiles data={twitterData["Housing"]} />
            )}
            <br></br>
            <br></br>
            <MapPolygon tag="Housing" postcode={""} />
            <br></br>
            <br></br>

            {lineIsLoading ? (
              <h1>Loading...</h1>
            ) : (
              <Line data={lineDataFinal} />
            )}

            <br></br>
            <br></br>
            <br></br>

            <br></br>
            <br></br>
            <br></br>
            <h1>Health Care</h1>
            <br />
            <br />
            <br />
            {isLoading ? (
              <h1>Loading...</h1>
            ) : (
              <GridTiles data={twitterData["Health care"]} />
            )}
            <br></br>
            <br></br>
            <Map tag="Health" postcode="" url={process.env.React_App_URL}></Map>
            <br></br>
            <br></br>
            <br></br>
            <br></br>
            <h1>Schools</h1>
            <br></br>
            <br></br>
            <br></br>
            {isLoading ? (
              <h1>Loading...</h1>
            ) : (
              <GridTiles data={twitterData["Education"]} />
            )}
            <br></br>
            <br></br>
            <Map tag="School" postcode=""></Map>
            <br></br>
            <br></br>
            <br></br>
            <h1>Entertainment</h1>
            <br></br>
            <br></br>
            <br></br>
            {isLoading ? (
              <h1>Loading...</h1>
            ) : (
              <GridTiles data={twitterData["Entertainment"]} />
            )}
            <br></br>
            <br></br>
            <br></br>
            <Map tag="Entertainment" postcode=""></Map>
            <br></br>
            <br></br>
            <h1>Environment</h1>
            <br></br>
            <br></br>
            <br></br>
            {isLoading ? (
              <h1>Loading...</h1>
            ) : (
              <GridTiles data={twitterData["Environment"]} />
            )}
            <br></br>
            <br></br>
            <br></br>
            <MapPolygon tag="Environment" postcode="" />

            <br></br>
            <br></br>
            <br></br>
            <h1>Table Summary</h1>
            <br></br>
           {tableIsLoading ? <h1>Loading...</h1>: <Pagination data={EntData} column={COLUMNS} />}
          </div>
        </div>
        <div
          className={toggleState === 2 ? "content  active-content" : "content"}
        >
          <h2>Postcode wise summary</h2>
          <br></br>
          <Dropdown selected={selected} setSelected={setSelected} />
          <br></br>

          <br></br>
          <br></br>
          <h1>Housing</h1>
          {postIsLoading ? (
            <h1>Loading...</h1>
          ) : (
            <Line data={postLineDataFinal} />
          )}
          {/* <Line data={postLineDataFinal} postcode={selected} /> */}
          <br></br>
          <br></br>
          <MapPolygon tag="Housing" postcode={selected} />
          <br></br>
          <br></br>
          <h1>Schools</h1>
          <br></br>
          <Map tag="School" postcode={selected}></Map>
          <br></br>
          <br></br>
          <h1>Health Care</h1>
          <br></br>
          <Map tag="Health" postcode={selected}></Map>
          <br></br>
          <br></br>
          <h1>Entertainment</h1>
          <br></br>
          <Map tag="Entertainment" postcode={selected}></Map>
          <br></br>
          <h1>Environment</h1>
          <br></br>
          <MapPolygon tag="Environment" postcode={selected} />
          <br></br>
          <br></br>
          <br></br>
        </div>
      </div>

      <div className="tweetsContainer"><StreamTweets/></div>

      
      

    </div>

    </div>
  );
};

export default App;
