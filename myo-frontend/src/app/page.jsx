"use client";
import Image from "next/image";
import styles from "./styling/homepage.module.css";
import ConnectButton from "./components/ConnectButton";
import VirtualKeyboard from "./components/VirtualKeyboard";
import React, { useState } from "react";

export default function Home() {
  const [dataFolder, setDataFolder] = useState("");
  const [nStages, setNStages] = useState("");
  return (
    <div className={styles.homepage}>
      <div className={styles.form}>
        <div className={styles.textinput}>
          Data folder:
          <input
            name="Name"
            className={styles.input}
            onChange={(e) => setDataFolder(e.target.value)}
          />
        </div>
        <div className={styles.textinput}>
          Number of stages:
          <input
            name="Name"
            className={styles.input}
            onChange={(e) => setNStages(e.target.value)}
          />
        </div>
      </div>

      <ConnectButton dataFolder={dataFolder} nStages={nStages} />
    </div>
  );
}
