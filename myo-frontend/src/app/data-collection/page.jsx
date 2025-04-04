"use client";

import styles from "../styling/datacollectionpage.module.css";
import React, { useEffect, useRef, useState } from "react";
import { Roboto_Mono } from "next/font/google";

const robotoMono = Roboto_Mono({
  subsets: ["latin"],
  weight: ["300", "700"],
});

export default function DataCollectionPage() {
  const [inputData, setInputData] = useState([]); // array of { char: string, correct: boolean }
  const [recording, setRecording] = useState(false);
  const recordingRef = useRef(false);

  const textPrompt = "the quick brown fox jumps over the lazy dog";

  const handleKeyDown = (e) => {
    if (!recordingRef.current && e.key === "Enter") {
      setRecording(true);
      recordingRef.current = true;

      fetch("http://localhost:5001/start-recording").catch((err) =>
        console.error("API error:", err)
      );
      return;
    }

    if (!recordingRef.current) return;

    if (e.key === "Backspace") {
      setInputData((prev) => prev.slice(0, -1));
      return;
    }

    if (e.key.length === 1) {
      const typedIndex = inputData.length;
      const expectedChar = textPrompt[typedIndex];
      const isCorrect = e.key === expectedChar;

      setInputData((prev) => [...prev, { char: e.key, correct: isCorrect }]);
    }
  };

  useEffect(() => {
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [inputData]);

  const renderedText = [];

  let promptIndex = 0;

  for (let i = 0; i < inputData.length; i++) {
    const { char, correct } = inputData[i];

    if (correct) {
      renderedText.push(
        <span key={`correct-${i}`} style={{ fontWeight: "bold" }}>
          {textPrompt[promptIndex]}
        </span>
      );
      promptIndex++;
    } else {
      renderedText.push(
        <span
          key={`incorrect-${i}`}
          style={{ color: "red", fontWeight: "bold" }}
        >
          {char}
        </span>
      );
    }
  }

  while (promptIndex < textPrompt.length) {
    renderedText.push(
      <span key={`remaining-${promptIndex}`}>{textPrompt[promptIndex]}</span>
    );
    promptIndex++;
  }

  return (
    <div className={styles.datacollectionpage}>
      {!recording && "Press Enter to start recording session"}
      <p className={robotoMono.className}>{renderedText}</p>
    </div>
  );
}
