const selectDept = document.getElementById("departemen");
const selectJabatan = document.getElementById("jabatan");

if (selectDept) {
  selectDept.addEventListener("change", function () {
    const deptId = this.value;

    selectJabatan.innerHTML = '<option value="">Loading...</option>';

    fetch("/api/jabatan/" + deptId)
      .then((response) => response.json())
      .then((data) => {
        selectJabatan.innerHTML = "";

        data.forEach((item) => {
          const option = document.createElement("option");
          option.value = item.id;
          option.text = item.nama;
          selectJabatan.appendChild(option);
        });
      });
  });
}
