function deleteProject(projectId) {
  fetch("/delete-project", {
    method: "POST",
    body: JSON.stringify({ proectId: projectId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}
