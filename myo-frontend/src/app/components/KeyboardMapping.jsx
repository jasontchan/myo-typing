"use client";
import React, { useState } from "react";

const keyboardRows = [
  ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
  ["a", "s", "d", "f", "g", "h", "j", "k", "l"],
  ["z", "x", "c", "v", "b", "n", "m"],
  ["        space        "],
];

const leftFingers = [
  "Left Pinky",
  "Left Ring",
  "Left Middle",
  "Left Index",
  "Left Thumb",
];
const rightFingers = [
  "Right Index",
  "Right Middle",
  "Right Ring",
  "Right Pinky",
  "Right Thumb",
];

const fingerColors = {
  "Left Pinky": "#FF6961",
  "Left Ring": "#FFB347",
  "Left Middle": "#FDFD96",
  "Left Index": "#77DD77",
  "Left Thumb": "#FFC0CB",
  "Right Index": "#AEC6CF",
  "Right Middle": "#779ECB",
  "Right Ring": "#CFCFC4",
  "Right Pinky": "#B39EB5",
  "Right Thumb": "#AA336A",
};

function KeyboardMapping({ keyMapping, setKeyMapping }) {
  const [activeFinger, setActiveFinger] = useState(null);

  const updateMapping = (key) => {
    if (!activeFinger) return;

    setKeyMapping((prevMapping) => {
      if (prevMapping[key] === activeFinger) {
        const updated = { ...prevMapping };
        delete updated[key];
        return updated;
      }
      return { ...prevMapping, [key]: activeFinger };
    });
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <div style={{ marginBottom: "20px" }}>
        <h3>Select a finger:</h3>
        <div style={{ marginBottom: "10px" }}>
          <strong>Left Hand:</strong>
          {leftFingers.map((finger) => (
            <button
              key={finger}
              onClick={() => setActiveFinger(finger)}
              style={{
                margin: "5px",
                padding: "10px",
                border:
                  activeFinger === finger
                    ? "2px solid black"
                    : "1px solid #ccc",
                borderRadius: "4px",
                backgroundColor: fingerColors[finger],
                cursor: "pointer",
              }}
            >
              {finger}
            </button>
          ))}
        </div>
        <div>
          <strong>Right Hand:</strong>
          {rightFingers.map((finger) => (
            <button
              key={finger}
              onClick={() => setActiveFinger(finger)}
              style={{
                margin: "5px",
                padding: "10px",
                border:
                  activeFinger === finger
                    ? "2px solid black"
                    : "1px solid #ccc",
                borderRadius: "4px",
                backgroundColor: fingerColors[finger],
                cursor: "pointer",
              }}
            >
              {finger}
            </button>
          ))}
        </div>
        {activeFinger && (
          <p style={{ marginTop: "10px" }}>
            Active Finger: <strong>{activeFinger}</strong>
          </p>
        )}
      </div>

      <div>
        {keyboardRows.map((row, rowIndex) => (
          <div
            key={rowIndex}
            style={{
              marginBottom: "10px",
              paddingLeft: `${
                rowIndex * 40 + Math.floor(rowIndex / 3) * 300
              }px`,
            }}
          >
            {row.map((char) => (
              <div
                key={char}
                onClick={() => updateMapping(char)}
                style={{
                  display: "inline-block",
                  margin: "5px",
                  textAlign: "center",
                  border: "1px solid #ccc",
                  padding: "10px",
                  minWidth: "50px",
                  cursor: activeFinger ? "pointer" : "default",
                  backgroundColor: keyMapping[char]
                    ? fingerColors[keyMapping[char]]
                    : "#fff",
                  borderRadius: "4px",
                }}
              >
                <div style={{ fontSize: "20px", fontWeight: "bold" }}>
                  {char.toUpperCase()}
                </div>
                <div style={{ fontSize: "12px", marginTop: "5px" }}>
                  {keyMapping[char] ? keyMapping[char] : "No mapping"}
                </div>
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}

export default KeyboardMapping;
