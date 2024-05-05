import { useState, useEffect, useRef } from "react";
import axios from "axios";
function App() {
  const [choice, setChoice] = useState("");
  const [description, setDesciption] = useState([]);
  const [precaution, setPrecaution] = useState([]);
  const [prediction, setPrediction] = useState([]);
  const [isPredicted, setIsPredicted] = useState(0);
  const [disease, setDisease] = useState("");
  const [desc, setDesc] = useState("");
  const [prec, setPrec] = useState("");
  const [flag, setFlag] = useState(0);
  const [symps, setSymps] = useState([]);
  const [input, setInput] = useState("");
  const ref = useRef();

  const sendData = () => {
    axios.post("http://127.0.0.1:5000/predict", { symps }).then((res) => {
      if (res.data != "") {
        setDisease(res.data);
        setIsPredicted(1);
      } else {
        setDisease(
          "Sorry ! we can not predict disease with only those symptomps"
        );
      }
      setFlag(1);
    });
  };

  const sendDiscData = () => {
    let data = {
      data: input,
    };
    axios.post("http://127.0.0.1:5000/desc", { data }).then((res) => {
      setDesc(res.data);
    });
    setFlag(1);
  };

  const sendPrec = () => {
    let data = {
      data: input,
    };
    axios.post("http://127.0.0.1:5000/prec", { data }).then((res) => {
      setPrec(res.data);
    });
    setFlag(1);
  };

  const genDes = () => {
    let data = [
      {
        you: "",
        robo: "Hello there ! Please type the disease name for you want to get description",
      },
    ];
    setDesciption(data);
  };
  const genPre = () => {
    let data = [
      {
        you: "",
        robo: "Hello there ! Please type the disease name for you want to get precaution",
      },
    ];
    setPrecaution(data);
  };
  const genPredict = () => {
    let data = [
      {
        you: "",
        robo: "Hello there ! Please type the symptomps name",
      },
    ];
    setPrediction(data);
  };
  useEffect(() => {
    if (ref.current) {
      ref.current.scrollIntoView();
    }
  }, [description, precaution, prediction]);

  useEffect(() => {
    if (choice == "2") {
      genDes();
    }
    if (choice == "3") {
      genPre();
    }
    if (choice == "1") {
      genPredict();
    }
  }, [choice]);

  const handleDesciption = () => {
    let data = {
      you: input,
      robo: "",
    };
    sendDiscData();
    setDesciption((m) => [...m, data]);
    setInput("");
  };

  const handlePrecaution = () => {
    let data = {
      you: input,
      robo: "",
    };
    sendPrec();
    setPrecaution((m) => [...m, data]);
    setInput("");
  };

  const handlePrediction = () => {
    let data = {};
    if (input == "no") {
      data = {
        you: input,
        robo: "",
      };
    } else {
      setSymps((m) => [...m, input]);
      data = {
        you: input,
        robo: "Do you have more symptomps",
      };
    }
    setPrediction((m) => [...m, data]);
    setInput("");
  };

  const handleForm = (e) => {
    e.preventDefault();
    if (choice == "2") {
      handleDesciption();
    }
    if (choice == "3") {
      handlePrecaution();
    }
    if (choice == "1") {
      handlePrediction();
    }
  };
  return (
    <div className="bg-gray-400 flex justify-center items-center h-screen">
      <div className="h-[80%] w-[60%] bg-white flex flex-col">
        <div className="h-[90%] bg-white w-full max-h-[90%] overflow-y-auto">
          {choice == "" ? (
            <>
              <div className="flex justify-start items-center w-full h-[15%] my-2">
                <div className="w-[35%] h-full bg-gray-200 flex items-center pl-5">
                  Hello ! How can i help you ?
                </div>
              </div>
              <div className="flex flex-col h-[30%] gap-2">
                <button
                  className="bg-blue-400 w-[25%] h-[30%] text-white"
                  onClick={() => setChoice(1)}
                >
                  Disease Prediction
                </button>
                <button
                  className="bg-blue-400 w-[25%] h-[30%] text-white"
                  onClick={() => setChoice(2)}
                >
                  Disease Desciption
                </button>
                <button
                  className="bg-blue-400 w-[25%] h-[30%] text-white"
                  onClick={() => setChoice(3)}
                >
                  Disease Precaution
                </button>
              </div>
            </>
          ) : (
            <>
              {choice == "2" ? (
                <>
                  {description.length > 0 &&
                    description.map((a, idx) => {
                      return (
                        <div key={idx}>
                          {a.you != "" && (
                            <div className="flex justify-end items-center w-full h-[15%] my-2">
                              <div className="w-[35%] h-24 bg-blue-400 text-white flex items-center pl-5">
                                {a.you}
                              </div>
                            </div>
                          )}
                          {a.robo != "" && (
                            <div className="flex justify-start items-center w-full h-[15%] my-2">
                              <div className="w-[35%] h-24 bg-gray-200 flex items-center pl-5">
                                {a.robo}
                              </div>
                            </div>
                          )}
                          {a.robo == "" && (
                            <div className="flex justify-start items-center w-full h-[15%] my-2">
                              <div className="w-[35%] min-h-24 bg-gray-200 flex items-center p-5">
                                {desc.length > 0 ? (
                                  <div>{desc}</div>
                                ) : (
                                  <div>
                                    Please check the spelling of disease if it
                                    is correct or not
                                  </div>
                                )}
                              </div>
                            </div>
                          )}
                        </div>
                      );
                    })}
                </>
              ) : (
                <>
                  {choice == "3" ? (
                    <>
                      {precaution.length > 0 &&
                        precaution.map((a, idx) => {
                          return (
                            <div key={idx}>
                              {a.you != "" && (
                                <div className="flex justify-end items-center w-full h-[15%] my-2">
                                  <div className="w-[35%] h-24 bg-blue-400 text-white flex items-center pl-5">
                                    {a.you}
                                  </div>
                                </div>
                              )}
                              {a.robo != "" && (
                                <div className="flex justify-start items-center w-full h-[15%] my-2">
                                  <div className="w-[35%] h-24 bg-gray-200 flex items-center pl-5">
                                    {a.robo}
                                  </div>
                                </div>
                              )}
                              {a.robo == "" && (
                                <div className="flex justify-start items-center w-full h-[15%] my-2">
                                  {prec.length > 0 ? (
                                    <div className="w-[35%] min-h-24 bg-gray-200 flex p-5 flex-col">
                                      <h2>Precautions are: </h2>
                                      <div>1.{prec[0]}</div>
                                      <div>2.{prec[1]}</div>
                                      <div>3.{prec[2]}</div>
                                      <div>4.{prec[3]}</div>
                                    </div>
                                  ) : (
                                    <div className="flex justify-start items-center w-full h-[15%] my-2">
                                      <div className="w-[35%] h-24 bg-gray-200 flex items-center pl-5">
                                        Please check the spelling of disease if
                                        it is correct or not
                                      </div>
                                    </div>
                                  )}
                                </div>
                              )}
                            </div>
                          );
                        })}
                    </>
                  ) : (
                    <>
                      {choice == "1" && (
                        <>
                          {prediction.length > 0 &&
                            prediction.map((a, idx) => {
                              return (
                                <div key={idx}>
                                  {a.you != "" && (
                                    <div className="flex justify-end items-center w-full h-[15%] my-2">
                                      <div className="w-[35%] h-24 bg-blue-400 text-white flex items-center pl-5">
                                        {a.you}
                                      </div>
                                    </div>
                                  )}
                                  {a.robo != "" && (
                                    <div className="flex justify-start items-center w-full h-[15%] my-2">
                                      <div className="w-[35%] h-24 bg-gray-200 flex items-center pl-5">
                                        {a.robo}
                                      </div>
                                    </div>
                                  )}
                                  {a.robo == "" && (
                                    <>
                                      {disease != "" ? (
                                        <div className="flex justify-start items-center w-full h-[15%] my-2">
                                          <div className="w-[35%] h-24 bg-gray-200 flex items-center pl-5">
                                            {isPredicted ? (
                                              <h2>You may have {disease}</h2>
                                            ) : (
                                              <h2>{disease}</h2>
                                            )}
                                          </div>
                                        </div>
                                      ) : (
                                        <button
                                          className="w-[35%] h-24 bg-gray-200"
                                          onClick={() => sendData()}
                                        >
                                          Click here for Predict
                                        </button>
                                      )}
                                    </>
                                  )}
                                </div>
                              );
                            })}
                        </>
                      )}
                    </>
                  )}
                </>
              )}
            </>
          )}
          <div ref={ref}></div>
        </div>
        {choice != "" && flag != 1 && (
          <form
            className="h-[10%] w-full flex justify-center items-center"
            onSubmit={(e) => handleForm(e)}
          >
            <input
              type="text"
              placeholder="Enter your response"
              className="w-3/4 h-3/4 border-black border px-2"
              value={input}
              onChange={(e) => setInput(e.target.value)}
            />
          </form>
        )}
      </div>
    </div>
  );
}

export default App;
