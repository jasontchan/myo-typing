"use client";

import styles from "../styling/datacollectionpage.module.css";
import React, { useEffect, useRef, useState } from "react";
import { Roboto_Mono } from "next/font/google";

const robotoMono = Roboto_Mono({
  subsets: ["latin"],
  weight: ["300", "700"],
});
export default function DataCollectionPage() {
  const [input, setInput] = useState("");
  const [recording, setRecording] = useState(false);
  const recordingRef = useRef(false);

  const textPrompt = "the quick brown fox jumps over the lazy dog";

  //create handleKeyDown event listener
  const handleKeyDown = (e) => {
    if (!recordingRef.current && e.key === "Enter") {
      setRecording(true);
      recordingRef.current = true;
      return;
    }
    if (recordingRef.current) {
      if (
        e.key.length === 1 &&
        input.length < textPrompt.length &&
        e.key === textPrompt[input.length]
      ) {
        //edit this to later capture exactly what user types including mistakes
        console.log("IN HERE");
        setInput((prev) => prev + e.key);
      }
    }
  };

  //useEffect mount the handleKeyDown event listener
  useEffect(() => {
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [input]);

  //create rendered text
  const renderedText = textPrompt.split("").map((char, index) => {
    let style = {};
    if (index < input.length) {
      style = { fontWeight: "bold" };
    }
    return (
      <span key={index} style={style}>
        {char}
      </span>
    );
  });

  return (
    <div className={styles.datacollectionpage}>
      {recording ? "" : "Press Enter to start recording session"}
      <p className={robotoMono.className}>{renderedText}</p>
    </div>
    //div that contains the rendered text from a file
  );
}
