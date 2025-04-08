"use client";

import styles from "../styling/datacollectionpage.module.css";
import React, { useEffect, useRef, useState } from "react";
import { Roboto_Mono } from "next/font/google";
import VirtualKeyboard from "../components/VirtualKeyboard";
import { useRouter } from "next/navigation";

const robotoMono = Roboto_Mono({
  subsets: ["latin"],
  weight: ["300", "700"],
});

export default function FinishCollectionPage() {
  const [keyMapping, setKeyMapping] = useState({});
  const [handedness, setHandedness] = useState("");
  const [age, setAge] = useState("");
  const [nClips, setNClips] = useState("");
  const [sessionConditions, setSessionConditions] = useState("");
  const router = useRouter();

  const saveMetadata = async (data) => {
    try {
      const response = await fetch("http://localhost:5001/save-metadata", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
      if (response.ok) {
        console.log("Object saved successfully on the server.");
      } else {
        console.error("Error saving object on the server.");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handleSave = () => {
    const metadata = {
      Handedness: handedness,
      Age: age,
      "Number of Clips": nClips,
      "Session Conditions": sessionConditions,
      "Key Mappings": keyMapping,
    };
    saveMetadata(metadata);
    router.push("/end-page");
  };

  return (
    <div className={styles.datacollectionpage}>
      {"Finished Recording"}
      <VirtualKeyboard keyMapping={keyMapping} setKeyMapping={setKeyMapping} />
      <div style={{ display: "flex", flexDirection: "column", rowGap: "10px" }}>
        <div style={{ display: "flex", flexDirection: "column" }}>
          Handedness
          <input
            type="text"
            style={{
              border: "1px solid #ccc",
              padding: "8px",
              borderRadius: "4px",
              fontSize: "16px",
              fontFamily: "sans-serif",
            }}
            onChange={(e) => setHandedness(e.target.value)}
          ></input>
        </div>
        <div style={{ display: "flex", flexDirection: "column" }}>
          Age
          <input
            type="text"
            style={{
              border: "1px solid #ccc",
              padding: "8px",
              borderRadius: "4px",
              fontSize: "16px",
              fontFamily: "sans-serif",
            }}
            onChange={(e) => setAge(e.target.value)}
          ></input>
        </div>
        <div style={{ display: "flex", flexDirection: "column" }}>
          Number of Clips
          <input
            type="text"
            style={{
              border: "1px solid #ccc",
              padding: "8px",
              borderRadius: "4px",
              fontSize: "16px",
              fontFamily: "sans-serif",
            }}
            onChange={(e) => setNClips(e.target.value)}
          ></input>
        </div>
        <div style={{ display: "flex", flexDirection: "column" }}>
          Session Conditions
          <input
            type="text"
            style={{
              border: "1px solid #ccc",
              padding: "8px",
              borderRadius: "4px",
              fontSize: "16px",
              fontFamily: "sans-serif",
            }}
            onChange={(e) => setSessionConditions(e.target.value)}
          ></input>
        </div>
      </div>

      <button onClick={handleSave}>Submit</button>
    </div>
  );
}
