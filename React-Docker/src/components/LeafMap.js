import {
  MapContainer as Map,
  Marker,
  Popup,
  TileLayer,
  useMap,
} from "react-leaflet";
import { Icon } from "leaflet";
import "leaflet/dist/leaflet.css";
import React, { useState, useEffect } from "react";
import axios from "axios";
import { Bar } from "react-chartjs-2";

export const icon = new Icon({
  iconUrl: "/marker.png",
  iconSize: [25, 25],
});

export const barIcon = new Icon({
  iconUrl: "/entertainment.png",
  iconSize: [25, 25],
});

export const carIcon = new Icon({
  iconUrl: "/marker-24.png",
  iconSize: [25, 25],
});

export const healthIcon = new Icon({
  iconUrl: "/healthcare.png",
  iconSize: [20, 20],
});

export const schoolIcon = new Icon({
  iconUrl: "/school.png",
  iconSize: [20, 20],
});

const LeafMap = (props) => {
  
  const [activeHospital, setActiveHospital] = React.useState(null);
  const [test, settest] = useState();

  const ResizeMap = () => {
    const map = useMap();
    map._onResize();
    return null;
  };

  const [isLoading, setIsLoading] = React.useState(true);
  const [healthData, setHealthData] = React.useState([]);
  const [schoolData, setSchoolData] = React.useState([]);
  const [EntData, setEntData] = React.useState([]);

  const [EntertainmentData, setEntertainmentData] = React.useState([]);

  var config = {
    method: "get",
    url:
      process.env.REACT_APP_URL +
      "/health_no_beds/_design/getHospitalData/_view/getHospitalData",
    headers: {
      Authorization: process.env.REACT_APP_USER,
    },
  };

  var schconfig = {
    method: "get",
    url:
      process.env.REACT_APP_URL +
      "/sch_rank/_design/getTopSchoolInfo/_view/getTopSchoolInfo",
    headers: {
      Authorization: process.env.REACT_APP_USER,
    },
  };

  var entconfig = {
    method: "get",
    url:
      process.env.REACT_APP_URL +
      "/liveability/_design/liveability/_view/liveabilityView",
    headers: {
      Authorization: process.env.REACT_APP_USER,
    },
  };

  if (props.tag === "School") {
    if (props.postcode !== "") {
      schconfig["url"] = schconfig["url"] + "?key=" + props.postcode;
    }
  }

  if (props.tag === "Health") {
    if (props.postcode !== "") {
      config["url"] = config["url"] + "?key=" + props.postcode;
    }
  }

  if (props.tag === "Entertainment") {
    if (props.postcode !== "") {
      entconfig["url"] = entconfig["url"] + "?key=" + props.postcode;
    }
  }

  React.useEffect(() => {
    var axios = require("axios");

    axios(config)
      .then((response) => {
        setHealthData(response.data);
      })
      .catch((error) => console.log(error));

    axios(schconfig)
      .then((response) => {
        setSchoolData(response.data);
      })
      .catch((error) => console.log(error));

    axios(entconfig)
      .then((response) => {
        setEntData(response.data);
      })
      .catch((error) => console.log(error));

    // axios(entconfig)
    // .then((response) =>  { setEntData(response.data)})
    // .catch((error) => console.log(error));
  }, [props.postcode]);

  React.useEffect(() => {
    if (
      healthData.length !== 0 &&
      schoolData.length !== 0 &&
      EntData.length !== 0
    ) {
      setIsLoading(false);
    }
  }, [healthData, schoolData, EntData, props.postcode]);

  if (props.tag === "Health") {
    return (
      <div>
        {isLoading ? (
          <h1>Loading...</h1>
        ) : (
          <Map center={[-37.813629, 144.963058]} zoom={12}>
            <ResizeMap />
            <TileLayer
              className="TileLayer"
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            />

            {healthData.rows.map((hospital) => (
              <Marker
                key={hospital.id}
                position={[hospital.value.lat, hospital.value.long]}
                icon={healthIcon}
              >
                <Popup position={[hospital.value.lat, hospital.value.long]}>
                  <div>
                    <h2>{hospital.value.hospital_name}</h2>
                    <p>{"Postcode : " + hospital.value.postcode}</p>
                    <p>{"Bed Category : " + hospital.value.bed_cat}</p>
                    <p>{"Number of Beds : " + hospital.value.no_beds}</p>
                  </div>
                </Popup>
              </Marker>
            ))}
          </Map>
        )}
      </div>
    );
  }

  if (props.tag === "School") {
    return (
      <div>
        {isLoading ? (
          <h1>Loading...</h1>
        ) : (
          <Map center={[-37.813629, 144.963058]} zoom={12}>
            <ResizeMap />
            <TileLayer
              className="TileLayer"
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution='&copy; <a href="http://osm.org/copyrightF">OpenStreetMap</a> contributors'
            />

            {schoolData.rows.length > 0 ? (
              schoolData.rows.map((school) => ({
                ...(school.value.properties_long &&
                school.value.properties_long !== null ? (
                  <Marker
                    key={school.id}
                    position={[
                      Number(school.value.properties_lat).toFixed(4),
                      Number(school.value.properties_long).toFixed(4),
                    ]}
                    icon={schoolIcon}
                  >
                    <Popup
                      position={[
                        school.value.properties_lat,
                        school.value.properties_lat,
                      ]}
                    >
                      <div>
                        <h2>{school.value.school_name}</h2>
                        <p>{"Postcode : " + school.key}</p>
                        <p>{"Sector : " + school.value.sector}</p>
                        <p>
                          {"Number of Enrollments : " +
                            school.value.enrollments}
                        </p>
                      </div>
                    </Popup>
                  </Marker>
                ) : (
                  <></>
                )),
              }))
            ) : (
              <></>
            )}
          </Map>
        )}
      </div>
    );
  }

  if (props.tag === "Entertainment" && props.postcode === "") {
    return (
      <div>
        {isLoading ? (
          <h1>Loading...</h1>
        ) : (
          <Map center={[-37.813629, 144.963058]} zoom={12}>
            <ResizeMap />
            <TileLayer
              className="TileLayer"
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution='&copy; <a href="http://osm.org/copyrightF">OpenStreetMap</a> contributors'
            />

            {EntData.rows.length > 0 ? (
              EntData.rows.map((entertainment) => ({
                ...(entertainment["value"]["bbox"][1] &&
                entertainment["value"]["bbox"][1] !== null ? (
                  <Marker
                    key={entertainment.value._id}
                    position={[
                      (entertainment["value"]["bbox"][1] +
                        entertainment["value"]["bbox"][3]) /
                        2,
                      (entertainment["value"]["bbox"][0] +
                        entertainment["value"]["bbox"][2]) /
                        2,
                    ]}
                    icon={barIcon}
                  >
                    <Popup
                      position={[
                        (entertainment["value"]["bbox"][1] +
                          entertainment["value"]["bbox"][3]) /
                          2,
                        (entertainment["value"]["bbox"][0] +
                          entertainment["value"]["bbox"][2]) /
                          2,
                      ]}
                    >
                      <div>
                        <h2>{entertainment.key}</h2>
                        <p>{"No of cafes : " + entertainment.value.no_cafe}</p>
                        <p>{"No of bars : " + entertainment.value.no_bar}</p>
                        <p>
                          {"No of sports facilities : " +
                            entertainment.value.no_sport_facilities}
                        </p>
                      </div>
                    </Popup>
                  </Marker>
                ) : (
                  <></>
                )),
              }))
            ) : (
              <></>
            )}
          </Map>
        )}
      </div>
    );
  }

  if (props.tag === "Entertainment" && props.postcode !== "") {
    var l1, l2, l3;

    // {
    //   EntData.rows.map((entertainment) => ({
    //     setcafeNumber(entertainment.value.no_cafe);
    //     // l1: entertainment.value.no_cafe,
    //     // l2: entertainment.value.no_bar,
    //     // l3: entertainment.value.no_sport_facilities,
    //   }));
    // }

    return (
      <div>
        {isLoading ? (
          <h1>Loading...</h1>
        ) : (
          <Bar
            data={{
              labels: [
                "Number of cafes",
                "Number of bars",
                "Number of sports facilities",
              ],
              datasets: [
                {
                  label: "Livablity Factor",
                  data: [
                    EntData.rows[0].value.no_cafe,
                    EntData.rows[0].value.no_bar,
                    EntData.rows[0].value.no_sport_facilities,
                  ],
                  backgroundColor: [
                    "rgba(54, 162, 235, 0.2)",
                    "rgba(255, 206, 86, 0.2)",
                    "rgba(75, 192, 192, 0.2)",
                    "rgba(153, 102, 255, 0.2)",
                    "rgba(255, 159, 64, 0.2)",
                    "rgba(54, 162, 235, 0.2)",
                    "rgba(255, 206, 86, 0.2)",
                    "rgba(75, 192, 192, 0.2)",
                    "rgba(153, 102, 255, 0.2)",
                    "rgba(255, 159, 64, 0.2)",
                  ],
                  borderColor: [
                    "rgba(54, 162, 235, 1)",
                    "rgba(255, 206, 86, 1)",
                    "rgba(75, 192, 192, 1)",
                    "rgba(153, 102, 255, 1)",
                    "rgba(255, 159, 64, 1)",
                    "rgba(54, 162, 235, 1)",
                    "rgba(255, 206, 86, 1)",
                    "rgba(75, 192, 192, 1)",
                    "rgba(153, 102, 255, 1)",
                    "rgba(255, 159, 64, 1)",
                  ],
                  borderWidth: 1,
                },
              ],
            }}
            height={400}
            width={300}
            options={{
              maintainAspectRatio: false,
              scales: {
                yAxes: [
                  {
                    ticks: {
                      beginAtZero: true,
                    },
                  },
                ],
              },
            }}
          />
        )}
      </div>
    );
  }
};

export default LeafMap;
