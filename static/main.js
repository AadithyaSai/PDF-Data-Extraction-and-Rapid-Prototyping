const alertBox = document.getElementById("alert-box");
const imageBox = document.getElementById("image-box");
const imageForm = document.getElementById("image-form");
const confirmBtn = document.getElementById("confirm-btn");
const input = document.getElementById("id_file");
const text = document.getElementById("text");
const csrf = document.getElementsByName("csrfmiddlewaretoken");

let tableData = {};

input.addEventListener("input", () => {
  input.classList.add("invisible");
  text.innerHTML = `<p>For best result, select only the table (without block headers). if there are no tables, select an empty area</p>`;
  alertBox.innerHTML = "";
  confirmBtn.classList.remove("invisible");

  const file_data = input.files[0];
  const url = URL.createObjectURL(file_data);

  // TODO: Fix PDF Rendering
  // $.ajax({
  //   type: "POST",
  //   url: "pdf2img",
  //   data: { csrfmiddlewaretoken: csrf[0].value, file: url },
  //   success: function (response) {
  //     console.log(response);
  //   },
  //   dataType: "json",
  // });

  imageBox.innerHTML = `<img src="${url}" id="image">`;

  const image = document.getElementById("image");
  const cropper = new Cropper(image, {
    crop(event) {
      tableData.x = Math.round(event.detail.x);
      tableData.y = Math.round(event.detail.y);
      tableData.w = Math.round(event.detail.width);
      tableData.h = Math.round(event.detail.height);
    },
  });
  confirmBtn.addEventListener("click", () => {
    cropper.getCroppedCanvas().toBlob((blob) => {
      const fd = new FormData();
      fd.append("csrfmiddlewaretoken", csrf[0].value);
      fd.append("file", file_data, "my-image.png");
      fd.append("table_data", JSON.stringify(tableData));

      $.ajax({
        type: "POST",
        url: imageForm.action,
        enctype: "multipart/form-data",
        data: fd,
        success: function (response) {
          text.innerHTML = "";
          //         alertBox.innerHTML = `<div class="alert alert-success"         role="alert">
          //  ${response.context.filter_predicted_result} was extracted from     the image.
          //   </div>`;

          window.location.href += "/result";
        },
        error: function (error) {
          alertBox.innerHTML = `<div class="alert alert-danger" role="alert">
     Oops! Something went wrong!
     </div>`;
        },
        cache: false,
        contentType: false,
        processData: false,
      });
    });
  });
});
