"use client";
import React, { useState } from "react";
import styles from "../styling/connectbutton.module.css";

function ConnectButton() {
  const [connect, setConnect] = useState(false);
  const handleClick = () => {
    setConnect(true);
  };

  return (
    <button className={styles.connectButton} onClick={handleClick}>
      Connect Myo Band
    </button>
  );
}

export default ConnectButton;
