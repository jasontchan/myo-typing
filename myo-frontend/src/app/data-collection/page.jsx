"use client";

import styles from "../styling/datacollectionpage.module.css";
import React, { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { Roboto_Mono } from "next/font/google";
import { generate, count } from "random-words";
import { useSearchParams } from "next/navigation";

const robotoMono = Roboto_Mono({
  subsets: ["latin"],
  weight: ["300", "700"],
});

export default function DataCollectionPage() {
  const [inputData, setInputData] = useState([]); // array of { char: string, correct: boolean }
  const [recording, setRecording] = useState(false);
  const [numIncorrect, setNumIncorrect] = useState(0);
  const recordingRef = useRef(false);
  const router = useRouter();
  const [textPrompt, setTextPrompt] = useState(generate(4).join(" "));
  const [nPrompts, setNPrompts] = useState(0);
  const searchParams = useSearchParams();
  const nStages = searchParams.get("nStages");
  const [nextPrompt, setNextPrompt] = useState(generate(4).join(" "));

  // const textPrompt = generate(5).join(" ");
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
      if (!isCorrect) {
        setNumIncorrect((prevCount) => prevCount + 1);
      }
    }
    const numCorrect = inputData.filter((item) => item.correct).length;
    if (recordingRef.current && numCorrect >= textPrompt.length) {
      //TODO: CHANGE THIS CONDITION
      setTextPrompt(nextPrompt);
      setNPrompts(nPrompts + 1);
      setInputData([]);
      setNextPrompt(generate(4).join(" "));
    }
  };

  useEffect(() => {
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [inputData]);

  const renderedText = [];
  const previewText = nextPrompt;

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

  useEffect(() => {
    // const numCorrect = inputData.filter((item) => item.correct).length;
    // if (numCorrect >= textPrompt.length) {
    //   //we are done!
    //   recordingRef.current = false; //edit
    //   fetch("http://localhost:5001/end-recording").catch((err) =>
    //     console.error("API error:", err)
    //   );
    //   router.push("/after-collection");
    //   return;
    // }
    if (nPrompts >= parseInt(nStages)) {
      //we are done!
      recordingRef.current = false; //edit
      fetch("http://localhost:5001/end-recording").catch((err) =>
        console.error("API error:", err)
      );
      router.push("/after-collection");
      return;
    }
  }, [inputData]);

  return (
    <div className={styles.datacollectionpage}>
      {!recording && "Press Enter to start recording session"}
      <div className={styles.promptArea}>
        <p className={robotoMono.className} style={{ margin: 0 }}>
          {renderedText}
        </p>
        <p className={robotoMono.className} style={{ margin: 0 }}>
          {previewText}
        </p>
      </div>
    </div>
  );
}
