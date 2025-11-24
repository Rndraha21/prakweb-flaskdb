const deptSelect = document.getElementById("departemen");
const jabatanSelect = document.getElementById("jabatan");

if (deptSelect && jabatanSelect) {
  deptSelect.addEventListener("change", async () => {
    const departemen = deptSelect.value;

    const response = await fetch(`/data_jabatan/${departemen}`);
    const jabatanList = await response.json();

    jabatanSelect.innerHTML =
      "<option value='' disabled selected>--Pilih Jabatan--</option>";

    jabatanList.forEach((jabatan) => {
      jabatanSelect.innerHTML += `<option value="${jabatan}">${jabatan}</option>`;
    });
  });
}
