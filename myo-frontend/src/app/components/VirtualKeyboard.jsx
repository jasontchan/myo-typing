"use client";
import React, { useState } from "react";

// Options for finger selection; an empty string indicates no selection.
const fingerOptions = [
  "",
  "Left Pinky",
  "Left Ring",
  "Left Middle",
  "Left Index",
  "Right Index",
  "Right Middle",
  "Right Ring",
  "Right Pinky",
];

// A simple QWERTY layout represented as rows.
const keyboardRows = [
  ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
  ["a", "s", "d", "f", "g", "h", "j", "k", "l"],
  ["z", "x", "c", "v", "b", "n", "m"],
];

// A component representing a single key.
function Key({ char, mapping, updateMapping }) {
  // Local state to control whether the key is in "edit mode."
  const [editing, setEditing] = useState(false);

  const handleClick = () => {
    setEditing(true);
  };

  // When the dropdown selection changes update the parent state and exit edit mode.
  const handleChange = (event) => {
    const value = event.target.value;
    updateMapping(char, value);
    setEditing(false);
  };

  return (
    <div
      style={{
        display: "inline-block",
        margin: "5px",
        textAlign: "center",
        border: "1px solid #ccc",
        padding: "10px",
        minWidth: "50px",
      }}
    >
      {!editing ? (
        <>
          <div
            style={{ fontSize: "20px", fontWeight: "bold", cursor: "pointer" }}
            onClick={handleClick}
          >
            {char.toUpperCase()}
          </div>

          <div style={{ fontSize: "12px", marginTop: "5px" }}>
            {mapping ? mapping : "No mapping"}
          </div>
        </>
      ) : (
        <select onChange={handleChange} defaultValue={mapping}>
          {fingerOptions.map((option, i) => (
            <option key={i} value={option}>
              {option === "" ? "Select finger" : option}
            </option>
          ))}
        </select>
      )}
    </div>
  );
}

function VirtualKeyboard({ keyMapping, setKeyMapping }) {
  //{ q: "Left Pinky", w: "Left Ring", ... }
  //   const [keyMapping, setKeyMapping] = useState({});

  const updateMapping = (key, finger) => {
    setKeyMapping((prevMapping) => ({ ...prevMapping, [key]: finger }));
  };

  return (
    <div>
      {keyboardRows.map((row, rowIndex) => (
        <div key={rowIndex} style={{ marginBottom: "10px" }}>
          {row.map((key) => (
            <Key
              key={key}
              char={key}
              mapping={keyMapping ? keyMapping[key] : ""}
              updateMapping={updateMapping}
            />
          ))}
        </div>
      ))}
    </div>
  );
}

export default VirtualKeyboard;
