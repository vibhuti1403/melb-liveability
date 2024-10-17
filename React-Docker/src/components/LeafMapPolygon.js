import {
  MapContainer as Map,
  Rectangle,
  Polygon,
  TileLayer,
  Tooltip,
  useMap,
  Pane,
  Marker,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";
import React from "react";
//import housingData from "./housing_get_latest_rai.json";
//import environmentData from "./getEnvData.json";
import { Icon } from "leaflet";

export const LeafMapPolygon = (props) => {
  
  const ResizeMap = () => {
    const map = useMap();
    map._onResize();
    return null;
  };

  const icon = new Icon({
    iconUrl: "/home.png",
    iconSize: [20, 20],
  });

  const iconClimate = new Icon({
    iconUrl: "/climate.png",
    iconSize: [25, 25],
  });

  const poly = [
    [-40, 144],
    [-35, 135],
  ];

  const colorArray = [
    "rgba(54, 162, 235, 0.7)",
    "rgba(255, 206, 86, 0.7)",
    "rgba(75, 192, 192, 0.7)",
    "rgba(153, 102, 255, 0.7)",
  ];

  const [isLoading, setIsLoading] = React.useState(true);
  const [environmentData, setEnvironmentData] = React.useState([]);
  const [housingData, setHousingData] = React.useState([]);

  var environmentconfig = {
    method: "get",
    url:
      process.env.REACT_APP_URL +
      "/env_pollutant/_design/getEnvData/_view/getEnvData",
    headers: {
      Authorization: process.env.REACT_APP_USER,
    },
  };

  var housingconfig = {
    method: "get",
    url:
      process.env.REACT_APP_URL +
      "/housing_rent_aff/_design/getLatestRAI/_view/getLatestRAI",
    headers: {
      Authorization: process.env.REACT_APP_USER,
    },
  };

  if (props.postcode !== "") {
    environmentconfig["url"] =
      environmentconfig["url"] + "?key=" + '"' + props.postcode + '"';
    housingconfig["url"] =
      housingconfig["url"] + "?key=" + '"' + props.postcode + '"';
  }

  React.useEffect(() => {
    var axios = require("axios");

    axios(environmentconfig)
      .then((response) => {
        setEnvironmentData(response.data);
      })
      .catch((error) => console.log(error));

    axios(housingconfig)
      .then((response) => {
        setHousingData(response.data);
      })
      .catch((error) => console.log(error));
  }, [props.postcode]);

  React.useEffect(() => {
    if (housingData.length !== 0 && environmentData.length !== 0) {
      setIsLoading(false);
    }
  }, [housingData, environmentData, props.postcode]);

  // const [isLoading, setIsLoading] = React.useState(true);
  // const [environmentData, setenvironmentData] = React.useState([]);
  // const [housingData, sethousingData] = React.useState([]);

  if (props.tag === "Environment") {
    return (
      <div>
        {isLoading ? (
          <h1>Loading...</h1>
        ) : (
          <Map center={[-37.813629, 144.963058]} zoom={13}>
            <ResizeMap />
            <TileLayer
              className="TileLayer"
              url="https://tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            />
            {environmentData.rows.map((environment) => (
              <Marker
                key={environment.id}
                position={[
                  environment["value"]["bbox"][1],
                  environment["value"]["bbox"][0],
                ]}
                icon={iconClimate}
              >
                <Tooltip>
                  <p>{environment["value"]["activities"]}</p>
                </Tooltip>
              </Marker>
            ))}
          </Map>
        )}
      </div>
    );
  }
  if (props.tag === "Housing") {
    return (
      <div>
        {isLoading ? (
          <h1>Loading...</h1>
        ) : (
          <Map center={[-37.813629, 144.963058]} zoom={11}>
            <ResizeMap />
            <TileLayer
              className="TileLayer"
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            />
            {housingData.rows.map((housing) => (
              <Marker
                key={housing.id}
                position={[
                  (housing["value"]["bbox"][1] + housing["value"]["bbox"][3]) /
                    2,
                  (housing["value"]["bbox"][0] + housing["value"]["bbox"][2]) /
                    2,
                ]}
                icon={icon}
              >
                <Tooltip>
                  <p>Postcode : {housing["value"]["postcode"]}</p>
                  <p>Latest RAI : {housing["value"]["latest_rai"]}</p>
                </Tooltip>
              </Marker>
            ))}
          </Map>
        )}
      </div>
    );
  }
};

export default LeafMapPolygon;
