"use client";
import React, { useState } from "react";
import { useRouter } from "next/navigation";
import styles from "../styling/connectbutton.module.css";

function ConnectButton() {
  const [connect, setConnect] = useState(false);
  const router = useRouter();
  const handleClick = () => {
    setConnect(true);
    //start myo band recording
    fetch("http://localhost:5001/start-connection")
      .then((response) => {
        if (!response.ok) {
          throw new Error("API call failed");
        }
        return response.json();
      })
      .then((data) => {})
      .catch((error) => {
        // throw new Error(error);
        console.log("error");
      });
    router.push("/data-collection");
  };

  return (
    <button className={styles.connectButton} onClick={handleClick}>
      Connect Myo Band
    </button>
  );
}

export default ConnectButton;
