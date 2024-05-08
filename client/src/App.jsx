import { useState, useEffect, useRef } from "react";
import axios from "axios";

export default function App() {
  const [input, setInput] = useState("");
  const [message, setMessage] = useState([
    { robo: "Welcome, may I know what symptoms are you facing ?", you: "" },
  ]);
  const [typing, setTyping] = useState(false);

  window.addEventListener("beforeunload", async () => {
    try {
      await axios.post("http://127.0.0.1:5000/reset");
    } catch (err) {
      console.log("Error");
    }
  });

  const ref = useRef();
  const sendData = async () => {
    setTyping(true);
    try {
      await axios
        .post("http://127.0.0.1:5000/predict", { symps: input })
        .then((res) => {
          const temp = {
            you: input,
            robo: res.data,
          };
          setMessage((prev) => [...prev, temp]);
        });
    } catch (err) {
      console.log("Error");
    } finally {
      setTyping(false);
    }
  };
  const onSubmit = (e) => {
    e.preventDefault();
    sendData();
    setInput("");
  };
  useEffect(() => {
    if (ref.current) {
      ref.current.scrollIntoView();
    }
  }, [message]);
  return (
    <div className="bg-gray-400 flex justify-center items-center h-screen flex-col">
      <div className="text-white text-2xl mb-5">MedAssist</div>
      <div className="h-[80%] w-[60%] bg-white flex flex-col">
        <div className="h-[90%] bg-white w-full max-h-[90%] overflow-y-auto">
          {message.length > 0 &&
            message.map((a, i) => {
              return (
                <div key={i}>
                  {a.you != "" && (
                    <div className="flex justify-end items-center w-full h-[15%] my-5">
                      <div className="w-[75%] h-24 bg-blue-400 text-white flex items-center pl-5">
                        <pre>{a.you}</pre>
                      </div>
                    </div>
                  )}
                  {a.robo != "" && (
                    <div className="flex justify-start items-center w-full h-[15%] my-5">
                      <div className="w-[75%] min-h-24 bg-gray-200 flex items-center pl-5">
                        <pre className="whitespace-pre-wrap py-5">{a.robo}</pre>
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          <div ref={ref}></div>
        </div>
        <form
          action=""
          className="h-[10%] w-full flex justify-center items-center gap-2"
          onSubmit={(e) => onSubmit(e)}
        >
          {typing && <div>ChatBot is Typing ....</div>}
          <input
            type="text"
            placeholder="Message MedAssist"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="w-3/4 h-3/4 border-black border px-2"
          />
        </form>
      </div>
    </div>
  );
}
