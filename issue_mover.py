from github import GitHub


gh = GitHub(username="bot-sunu", password="password123!@#")
oh_issues = gh.repos(
    "openhatch")("oh-mainline").issues.get(
    state="all", labels="bugimporters", per_page=50)

total_issues = len(oh_issues)

for index, issue in enumerate(oh_issues):
    print "Processing issue #%i of %i" % (index+1, total_issues)
    title = issue.get("title")
    body = issue.get("body")

    assignee = issue["assignee"]["login"] if issue.get("assignee") else None
    milestone = issue.get('milestone')
    state = issue.get("state")

    labels = [label['name'] for label in issue['labels']]

    comment_count = issue.get("comments")
    if comment_count > 0:
        comments = gh.repos(
            "openhatch")("oh-mainline").issues(issue["number"]).comments.get()
        for comment in comments:
            comment_body = comment.get("body")
            creator = comment.get("user")["login"]
            creation_time = comment.get("created_at")
            text = "<hr/> **%s** commented at %s: <br/> %s" % (
                creator, creation_time, comment_body)
            body = body + text

    new_issue = gh.repos("bot-sunu")("test-repo").issues.post(
        title=title, body=body, assignee=assignee, milestone=milestone,
        labels=labels)
    if state == "closed":
        gh.repos("bot-sunu")("test-repo").issues(
            new_issue["number"]).patch(state="closed")
