function getFingerprint() {
  return new Promise(resolve => {
    if (window.requestIdleCallback) {
      requestIdleCallback(() => {
        Fingerprint2.get(resolve);
      });
    } else {
      setTimeout(() => {
        Fingerprint2.get(resolve);
      }, 500);
    }
  });
}

async function main() {
  const response = await fetch(`/validate/${token}`, {
    method: 'post',
  });

  if (response.status !== 204) {
    alert('Invalid token');
    return;
  }

  const loaderEl = document.querySelector('.loader');
  loaderEl.appendChild(document.createTextNode('Loading... Please do not close this window.'));

  const fingerprints = [];

  for (let i = 0; i < 5; i += 1) {
    const fingerprint = await getFingerprint();
    const hash = objectHash(fingerprint);
    fingerprints.push(hash);
  }

  await fetch('/fingerprints', {
    method: 'post',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ token, fingerprints }),
  });

  while (loaderEl.firstChild) {
    loaderEl.removeChild(loaderEl.firstChild);
  }

  loaderEl.appendChild(document.createTextNode("That's it! You may close this window."));
}
main();
