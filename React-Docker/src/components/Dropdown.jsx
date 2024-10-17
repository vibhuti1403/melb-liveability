import { useState } from "react";
import React from "react";
import { Icon } from "semantic-ui-react";
// import PostCodedata from "./housing_get_latest_rai.json";

//function Dropdown({ selected, setSelected }) {

export const Dropdown = (props) => {
  const [isLoading, setIsLoading] = React.useState(true);
  const [housingData, setHousingData] = React.useState([]);
  const [isActive, setIsActive] = useState(false);
  if (props.selected == "") props.setSelected("3053");

  var housingconfig = {
    method: "get",
    url:
      process.env.REACT_APP_URL +
      "/housing_rent_aff/_design/getLatestRAI/_view/getLatestRAI",
    headers: {
      Authorization: process.env.REACT_APP_USER,
    },
  };

  React.useEffect(() => {
    var axios = require("axios");

    axios(housingconfig)
      .then((response) => {
        setHousingData(response.data);
      })
      .catch((error) => console.log(error));
  });

  React.useEffect(() => {
    if (housingData.length !== 0) {
      setIsLoading(false);
    }
  }, [housingData]);

  return (
    <div className="dropdown">
      <div
        className="dropdown-btn"
        onClick={(e) => setIsActive(!isActive)}
      >
        {props.selected}
        <link
          rel="stylesheet"
          href="https://maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css"
        ></link>
        <i className="fa fa-caret-down"></i>
      </div>
      {isActive && (
        <div className="dropdown-content">
          {housingData.rows.map((option) => (

            // console.log(option.value.postcode)
            <div
              onClick={(e) => {
                props.setSelected(option.value.postcode);
                setIsActive(false);
              }}
              className="dropdown-item"
            >
              {option.value.postcode}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Dropdown;
