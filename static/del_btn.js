const del_btns = document.querySelectorAll("[data-delete-url]");
function deleteItem(event) {
  const url = event.currentTarget.attributes.getNamedItem("data-delete-url")
    .value;
  fetch(url, {
    method: "DELETE",
    redirect: "manual"
  }).then(response => {
    location.reload();
  });
}
for (const btn of del_btns) {
  btn.addEventListener("click", deleteItem);
}
