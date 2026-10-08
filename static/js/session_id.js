export function getSessionId() {
  let sid = localStorage.getItem("vet_session_id");
  if (!sid) {
    sid = "vet-" + crypto.randomUUID().slice(0, 18);
    localStorage.setItem("vet_session_id", sid);
  }
  return sid;
}
