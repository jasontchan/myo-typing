import Image from "next/image";
import styles from "./styling/homepage.module.css";
import ConnectButton from "./components/ConnectButton";

export default function Home() {
  return (
    <div className={styles.homepage}>
      <div className={styles.form}>
        <div className={styles.textinput}>
          Name:
          <input name="Name" className={styles.input} />
        </div>
        <div className={styles.textinput}>
          Session Length:
          <input name="Name" className={styles.input} />
        </div>
      </div>

      <ConnectButton />
    </div>
  );
}
