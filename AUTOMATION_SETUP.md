# Automated Map Updates from Microsoft Forms

This guide explains how to set up automatic updates to the Business History Academic Map when someone submits the Microsoft Form.

## Architecture

```
Microsoft Form → Power Automate → GitHub Actions → academics_data.json → GitHub Pages
     (1)              (2)              (3)                (4)               (5)
```

1. **Microsoft Form**: Academic submits opt-in/withdrawal form
2. **Power Automate**: Detects submission, sends webhook to GitHub
3. **GitHub Actions**: Processes data, geocodes location, updates JSON
4. **academics_data.json**: Updated with new/removed individual
5. **GitHub Pages**: Automatically deploys updated map

## Prerequisites

- Microsoft 365 account (for Power Automate)
- GitHub account with access to this repository
- GitHub Personal Access Token (PAT)

---

## Step 1: Create a GitHub Personal Access Token

1. Go to [GitHub Settings > Developer settings > Personal access tokens > Fine-grained tokens](https://github.com/settings/tokens?type=beta)

2. Click **"Generate new token"**

3. Configure the token:
   - **Token name**: `power-automate-map-updates`
   - **Expiration**: Choose an appropriate duration (recommend 1 year)
   - **Repository access**: Select "Only select repositories" → choose `business-history-map`
   - **Permissions**:
     - **Contents**: Read and Write
     - **Metadata**: Read-only

4. Click **"Generate token"** and **copy the token immediately** (you won't see it again)

---

## Step 2: Set Up Power Automate Flow

### 2.1 Create a New Flow

1. Go to [Power Automate](https://make.powerautomate.com/)
2. Click **"Create"** → **"Automated cloud flow"**
3. Name: `Business History Map - Form Submission`
4. Choose trigger: **"When a new response is submitted"** (Microsoft Forms)
5. Click **"Create"**

### 2.2 Configure the Trigger

1. In the trigger block, select your Microsoft Form from the dropdown
2. Form ID: Select your Business History Academic Directory form

### 2.3 Add "Get response details" Action

1. Click **"+ New step"**
2. Search for **"Get response details"** (Microsoft Forms)
3. Configure:
   - Form ID: Same form as above
   - Response ID: Select "Response Id" from dynamic content

### 2.4 Add HTTP Action (GitHub Webhook)

1. Click **"+ New step"**
2. Search for **"HTTP"** and select the HTTP action
3. Configure:

   - **Method**: `POST`

   - **URI**:
     ```
     https://api.github.com/repos/stephdeck/business-history-map/dispatches
     ```

   - **Headers**:
     | Key | Value |
     |-----|-------|
     | Accept | application/vnd.github.v3+json |
     | Authorization | Bearer YOUR_GITHUB_TOKEN |
     | Content-Type | application/json |

   - **Body** (click "Show advanced options" if needed):
     ```json
     {
       "event_type": "form-submission",
       "client_payload": {
         "action": "@{if(contains(toLower(body('Get_response_details')?['QUESTION_ID_FOR_ACTION']), 'withdraw'), 'withdraw', 'add')}",
         "name": "@{body('Get_response_details')?['QUESTION_ID_FOR_NAME']}",
         "affiliation": "@{body('Get_response_details')?['QUESTION_ID_FOR_AFFILIATION']}",
         "city": "@{body('Get_response_details')?['QUESTION_ID_FOR_CITY']}",
         "country": "@{body('Get_response_details')?['QUESTION_ID_FOR_COUNTRY']}",
         "interests": "@{body('Get_response_details')?['QUESTION_ID_FOR_INTERESTS']}"
       }
     }
     ```

### 2.5 Map Your Form Questions

Replace the `QUESTION_ID_FOR_*` placeholders with your actual form field IDs.

In Power Automate, when you click in the Body field:
1. Click **"Add dynamic content"**
2. You'll see your form questions listed
3. Click each one to insert it in the correct place

**Example mapping** (your question IDs will differ):
- Name field → Replace `QUESTION_ID_FOR_NAME`
- Affiliation field → Replace `QUESTION_ID_FOR_AFFILIATION`
- City field → Replace `QUESTION_ID_FOR_CITY`
- Country field → Replace `QUESTION_ID_FOR_COUNTRY`
- Research interests field → Replace `QUESTION_ID_FOR_INTERESTS`
- Action/Request type field → Replace `QUESTION_ID_FOR_ACTION`

### 2.6 Save and Test

1. Click **"Save"**
2. Submit a test entry in your Microsoft Form
3. Go to Power Automate → "My flows" → click your flow → "Run history"
4. Check if the run succeeded

---

## Step 3: Verify GitHub Actions

After a successful Power Automate run:

1. Go to your [GitHub repository Actions tab](https://github.com/stephdeck/business-history-map/actions)
2. You should see a new workflow run triggered
3. Click on it to see the processing logs
4. Check that `academics_data.json` was updated

---

## Testing Without Power Automate

You can manually test the GitHub Action:

1. Go to [Actions](https://github.com/stephdeck/business-history-map/actions)
2. Click **"Update Map Data"** workflow
3. Click **"Run workflow"**
4. Fill in test data:
   - Action: `add` or `withdraw`
   - Name: `Test Person`
   - Affiliation: `Test University`
   - City: `London`
   - Country: `UK`
   - Interests: `testing, automation`
5. Click **"Run workflow"**

---

## Troubleshooting

### Power Automate shows "Unauthorized" error
- Your GitHub token may have expired
- Regenerate the token and update the Authorization header

### GitHub Action fails
- Check the Actions logs for specific error messages
- Verify the JSON payload format is correct
- Ensure the repository has write permissions enabled for Actions

### Geocoding fails
- The script uses OpenStreetMap Nominatim (free)
- Check if the city/country spelling is correct
- The entry will still be added with approximate coordinates

### Person not appearing on map
- Check the browser console for JavaScript errors
- Verify the entry was added to `academics_data.json`
- Clear browser cache and refresh

---

## Form Field Recommendations

For optimal automation, your Microsoft Form should include:

1. **Action/Request Type** (choice)
   - "Add me to the map"
   - "Remove me from the map"

2. **Full Name** (text)
   - Required

3. **Affiliation/Institution** (text)
   - Required for "Add" action

4. **City** (text)
   - Required for "Add" action

5. **Country** (text or dropdown)
   - Required for "Add" action

6. **Research Interests** (text, long answer)
   - Optional

---

## Security Notes

- The GitHub token has minimal permissions (only this repo)
- Form submissions are validated before processing
- No sensitive data is stored or transmitted
- All updates are tracked in Git commit history

---

## Maintenance

### Renewing the GitHub Token
Before your token expires:
1. Generate a new token following Step 1
2. Update the Authorization header in Power Automate
3. Delete the old token

### Updating the Processing Script
If you need to modify how submissions are processed:
1. Edit `scripts/process_submission.py`
2. Commit and push to the repository
3. Future form submissions will use the updated logic
