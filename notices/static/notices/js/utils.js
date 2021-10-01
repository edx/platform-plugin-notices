const ACKNOWLEDGMENT_TYPES = {
  DISMISSED: "dismissed",
  CONFIRMED: "confirmed"
}

function confirmNoticeClick(){
  sendAcknowledgment(ACKNOWLEDGMENT_TYPES.CONFIRMED, forwardingUrl)
}

function dismissNoticeClick(event){
  let nextUrl;
  if (event.target.href){
    // If caller is a link, stop redirection until after API call.
    event.preventDefault();
    nextUrl = event.target.href;
  } else {
    nextUrl = forwardingUrl;
  }
  sendAcknowledgment(ACKNOWLEDGMENT_TYPES.DISMISSED, nextUrl)
};

function sendAcknowledgment(type, url){
  const callback = () => {
    window.location = url;
  }
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  let params = { notice_id: noticeId, acknowledgment_type: type};
  let postRequest = new XMLHttpRequest();
  postRequest.open("POST", "/notices/api/v1/acknowledge");
  postRequest.setRequestHeader("Content-type", "application/json");
  postRequest.setRequestHeader("X-CSRFToken", csrftoken);
  postRequest.send(JSON.stringify(params));
  postRequest.onreadystatechange = () => {
    if (postRequest.readyState === 4 && postRequest.status === 204) {
      console.log("acknowledgment successful");
      callback();
    }
  };
}