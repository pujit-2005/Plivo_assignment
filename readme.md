# InspireWorks - Plivo IVR & OTP Authentication System

A communication application built with Python, Flask, and the Plivo Voice API for InspireWorks. The system initiates outbound calls, authenticates callers using a 4-digit DTMF OTP, and navigates a multi-level Interactive Voice Response (IVR) menu with audio playback and call forwarding.

## Features

* **Outbound Calling**: Programmatically triggers calls from a designated Plivo phone number to a target phone number.


* **OTP Authentication**: Prompts callers for a 4-digit DTMF OTP (birthdate in `DDMM` format) and re-prompts on incorrect entries until authenticated.


* **Multi-Level IVR Menu**:
* **Level 1**: Language selection (Press 1 for English / Press 2 for Spanish).


* **Level 2**: Branching options to play an audio file (Press 1) or forward the call to a live associate (Press 2).




* **Dynamic Call Flow**: Uses Plivo XML to manage call logic and handle invalid inputs gracefully.



## Prerequisites

* Python 3.8+
* [ngrok](https://ngrok.com/) for exposing local webhook endpoints to the public internet
* Active Plivo credentials



## Configuration & Credentials

The application uses the following configuration parameters inside `app.py`:

* **Auth ID**: `MAMTAWMGIOMZCTNTYZZS`

* **Auth Token**: `M2Y2MzIIMWEtOGU5Ny00YzYxLWFkNzItZmE5ZmNI`

* **Plivo Source Number**: `+918035454161`

* **Live Associate Number**: `02264236412`

* **Target Phone Number (`MY_NUMBER`)**: Receiver's phone number formatted with country code (e.g., `+91XXXXXXXXXX`).


* **Hardcoded OTP (`HARDCODED_OTP`)**: Birthdate in `DDMM` format (e.g., `1503`).


* **Base Webhook URL (`BASE_URL`)**: Active ngrok HTTPS tunnel URL (e.g., `[https://your-tunnel.ngrok-free.dev](https://your-tunnel.ngrok-free.dev)`).

## Setup & Local Execution

1. **Clone the Repository**:
```bash
git clone https://github.com/pujit-2005/Plivo_assignment.git
cd Plivo_assignment

```


2. **Install Dependencies**:
```bash
pip install flask plivo

```


3. **Start ngrok Tunnel**:
```bash
ngrok http 5000

```


Copy the generated HTTPS forwarding URL and update the `BASE_URL` variable in `app.py`.
4. **Launch Application**:
```bash
python app.py

```



## Testing the Call Flow

1. **Initiate Outbound Call**: Navigate to `http://localhost:5000/make_call` in your browser.


2. **OTP Verification**:
* Answer the call received from `+918035454161`.


* Enter an incorrect 4-digit code to test error handling.


* Enter the correct `DDMM` birthdate to authenticate.




3. **Navigate IVR**:
* **Level 1**: Press `1` for English or `2` for Spanish.


* **Level 2**: Press `1` to listen to audio playback or `2` to forward the call to the live associate (`02264236412`).