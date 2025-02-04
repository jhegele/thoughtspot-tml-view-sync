# ThoughtSpot TML View Sync Example

This sample code provides an example of how to sync views between TML when programmatically promoting TML from a dev environment to a prod environment.

## How to use this code

1. Clone this repository
2. Run `pip install -r requirements.txt` to install dependencies
3. Create the following environment variables:

   - `TS_USERNAME`: Username used to access your ThoughtSpot cluster
   - `TS_SECRET_KEY`: Secret key from your ThoughtSpot cluster (note that you may need to use a different auth method if you do not have access to a secret key)
   - `TS_HOST`: The host portion of your ThoughtSpot cluster URL. This will typically be in the form `https://my-cluster.thoughtspot.cloud` (note, do not include the trailing /).
   - `TS_LIVEBOARD_GUID_DEV`: The GUID of your dev liveboard. This liveboard **will not have** user views and changes to this liveboard will be "pushed" to your prod liveboard.
   - `TS_LIVEBOARD_GUID_PROD`: The GUID of your prod liveboard. This liveboard **will** have user views.

4. Run `python sync.py` to run the script

## Overview

### The challenge

Many ThoughtSpot users want a flow where they produce and manage liveboards in a dev environment and, once those liveboards are sufficiently tested they can be "promoted" to a prod environment where end users can make use of them. This promotion typically happens via TML export/import (export TML from dev, import to prod). This flow works as expected when the liveboard is net new to the prod environment. However, if a liveboard already exists in prod, updates are made in dev, and then those updates are promoted to prod via TML import this will wipe out any user views that were defined on the prod liveboard.

### The solution

In a situation where updates are being promoted from dev to prod, we can leverage the existing prod TML and replicate the views into our dev TML prior to pushing it to prod. The general flow we'll use is:

1. Download dev TML to be promoted
2. Download prod TML with existing user views
3. Copy user views from prod TML to dev TML
4. Push dev TML to prod

## Requirements

- Python (`3.6` or above)

## A note on authentication

ThoughtSpot provides multiple ways to authenticate via API. In this code sample I am using username + secret key to get a full access token. You can also use username + password to generate a full access token. There is no inherent advantage/benefit to using the secret key, it's simply the option that I have available to me for the cluster I built this against. So the precise method is left to you to determine. You'll just need to make sure that the method you use generates a token that can be used for subsequent api calls.

## Environent variables

I leverage environment variables here to avoid committing sensitive info to Github. In general this is a good idea and, if you are committing this code to your own version control platform it's something you should **absolutely** do. However, if you are just hacking around and testing it's not strictly necessary.
