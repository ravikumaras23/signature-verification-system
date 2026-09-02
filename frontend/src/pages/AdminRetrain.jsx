import {
  useState
} from "react";

import {
  Brain,
  Upload,
  CheckCircle2,
  AlertTriangle
} from "lucide-react";

import API from "../api";

import Header
  from "../components/Header";


export default function AdminRetrain() {

  const [
    genuineImages,
    setGenuineImages
  ] = useState([]);

  const [
    forgedImages,
    setForgedImages
  ] = useState([]);

  const [
    epochs,
    setEpochs
  ] = useState(10);

  const [
    loading,
    setLoading
  ] = useState(false);

  const [
    result,
    setResult
  ] = useState(null);

  const [
    error,
    setError
  ] = useState("");


  const startRetraining =
    async () => {

      setError("");
      setResult(null);


      if (
        genuineImages.length === 0
        &&
        forgedImages.length === 0
      ) {

        setError(
          "Upload at least one image."
        );

        return;
      }


      setLoading(true);


      try {

        const formData =
          new FormData();


        genuineImages.forEach(
          image => {

            formData.append(
              "genuine_images",
              image
            );

          }
        );


        forgedImages.forEach(
          image => {

            formData.append(
              "forged_images",
              image
            );

          }
        );


        formData.append(
          "epochs",
          epochs
        );


        const response =
          await API.post(
            "/admin/retrain/",
            formData,
            {
              headers: {
                "Content-Type":
                  "multipart/form-data"
              },
              timeout:
                0
            }
          );


        setResult(
          response.data
        );


        setGenuineImages(
          []
        );

        setForgedImages(
          []
        );


      } catch (err) {

        setError(
          err.response
            ?.data
            ?.error
          ||
          "Model retraining failed."
        );

      } finally {

        setLoading(false);

      }
    };


  return (
    <>
      <Header
        title="Retrain Model"
      />


      <div className="page">


        <div className="page-heading">

          <div>

            <span className="eyebrow">
              MODEL MANAGEMENT
            </span>

            <h2>
              Retrain AI model
            </h2>

            <p>
              Add new signature examples
              and fine-tune the existing
              model.
            </p>

          </div>

        </div>


        <div className="retrain-warning">

          <AlertTriangle
            size={18}
          />

          <div>

            <strong>
              Important
            </strong>

            <p>
              Upload images with the
              correct class. Existing
              training data is retained,
              and the current model is
              backed up before replacement.
            </p>

          </div>

        </div>


        <div className="retrain-grid">


          <div className="dashboard-card">

            <div className="card-heading">

              <div>

                <h3>
                  Genuine signatures
                </h3>

                <p>
                  Upload authentic
                  signatures
                </p>

              </div>

              <div className="class-badge genuine">
                Genuine
              </div>

            </div>


            <label className="retrain-upload">

              <Upload
                size={24}
              />

              <strong>
                Select genuine images
              </strong>

              <span>
                You can select multiple
                images
              </span>

              <input
                type="file"
                accept="image/*"
                multiple
                hidden
                onChange={e =>
                  setGenuineImages(
                    Array.from(
                      e.target.files
                    )
                  )
                }
              />

            </label>


            <div className="file-count">

              {genuineImages.length}

              {" "}

              image(s) selected

            </div>

          </div>


          <div className="dashboard-card">

            <div className="card-heading">

              <div>

                <h3>
                  Forged signatures
                </h3>

                <p>
                  Upload fraudulent
                  signatures
                </p>

              </div>

              <div className="class-badge forged">
                Forged
              </div>

            </div>


            <label className="retrain-upload">

              <Upload
                size={24}
              />

              <strong>
                Select forged images
              </strong>

              <span>
                You can select multiple
                images
              </span>

              <input
                type="file"
                accept="image/*"
                multiple
                hidden
                onChange={e =>
                  setForgedImages(
                    Array.from(
                      e.target.files
                    )
                  )
                }
              />

            </label>


            <div className="file-count">

              {forgedImages.length}

              {" "}

              image(s) selected

            </div>

          </div>

        </div>


        <div className="dashboard-card retrain-settings">

          <div className="training-icon">

            <Brain
              size={23}
            />

          </div>


          <div className="training-info">

            <h3>
              Training settings
            </h3>

            <p>
              The existing model will
              be fine-tuned using the
              complete training dataset.
            </p>

          </div>


          <div className="epoch-control">

            <label>
              Epochs
            </label>

            <input
              type="number"
              min="1"
              max="50"
              value={epochs}
              onChange={e =>
                setEpochs(
                  e.target.value
                )
              }
            />

          </div>

        </div>


        {error && (

          <div className="form-error">

            {error}

          </div>

        )}


        <button
          className="retrain-button"
          disabled={loading}
          onClick={
            startRetraining
          }
        >

          <Brain
            size={18}
          />

          {loading
            ? "Retraining model..."
            : "Start model retraining"}

        </button>


        {result && (

          <div className="retrain-result">

            <div className="success-icon">

              <CheckCircle2
                size={27}
              />

            </div>


            <div>

              <h3>
                Model retrained successfully
              </h3>

              <p>
                New signature images
                have been incorporated
                into the model.
              </p>


              <div className="training-results">

                <span>
                  Uploaded Genuine:
                  <strong>
                    {
                      result.uploaded
                        ?.genuine
                    }
                  </strong>
                </span>


                <span>
                  Uploaded Forged:
                  <strong>
                    {
                      result.uploaded
                        ?.forged
                    }
                  </strong>
                </span>


                <span>
                  Training Accuracy:
                  <strong>
                    {
                      result.training
                        ?.accuracy
                    }%
                  </strong>
                </span>


                <span>
                  Validation Accuracy:
                  <strong>
                    {
                      result.training
                        ?.validation_accuracy
                    }%
                  </strong>
                </span>

              </div>

            </div>

          </div>

        )}

      </div>

    </>
  );
}