import React from "react";
import GenericTile from "react-generic-tile";
import { FiUsers } from "react-icons/fi";
import { AiOutlineTwitter } from "react-icons/ai";
import RGL, { WidthProvider } from "react-grid-layout";

const ReactGridLayout = WidthProvider(RGL);
const gridProps = {
  items: 5,
  rowHeight: 30,
  preventCollision: false,
  compactType: null,
  cols: 12,
};
const GridTiles = (props) => {
  var Negative = props.data["Negative"];
  var Neutral = props.data["Neutral"];
  var Positive = props.data["Positive"];
  const Total = Negative + Neutral + Positive;

  Negative = ((Negative / Total) * 100).toFixed(2) + "%";
  Neutral = ((Neutral / Total) * 100).toFixed(2) + "%";
  Positive = ((Positive / Total) * 100).toFixed(2) + "%";
  return (
    <ReactGridLayout {...gridProps}>
      <div key="1" data-grid={{ x: 0, y: 0, w: 3, h: 3, static: false }}>
        <GenericTile
          header="Total Tweets"
          icon={<AiOutlineTwitter size={32} color="#00acee" />}
          number={Total}
        />
      </div>
      <div key="2" data-grid={{ x: 3, y: 0, w: 3, h: 3, static: false }}>
        <GenericTile
          key="2"
          header="Positive Sentiments"
          icon={<FiUsers size={28} />}
          number={Positive}
          color="Good"
          indicator="Up"
        />
      </div>
      <div key="3" data-grid={{ x: 6, y: 0, w: 3, h: 3, static: false }}>
        <GenericTile
          header="Negative Sentiments"
          icon={<FiUsers size={28} />}
          number={Negative}
          color="Bad"
          indicator="Down"
        />
      </div>
      <div key="4" data-grid={{ x: 12, y: 0, w: 3, h: 3, static: false }}>
        <GenericTile
          header="Neutral Sentiments"
          icon={<FiUsers size={28} />}
          number={Neutral}
          color="Warning"
        />
      </div>
    </ReactGridLayout>
  );
};

export default GridTiles;
