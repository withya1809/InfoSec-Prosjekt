package assignment2.issueresolver;

/* Faculty is a super class for the StudentAssistant, Professor, and HeadofTheDepartment classes. It is implemented as an
 * abstract class, since there should be no reason to instantiated an Faculty type directly.
 */
abstract class Faculty {
	private Issue currentIssue = null;
	protected Rank r;
	private IssueHandler issueHandler;

	public Faculty(IssueHandler handler) {
		issueHandler = handler;
	}

	/* Start the conversation */
	public void receiveIssue(Issue issue) {
		currentIssue = issue;
		issue.setHandler(this);
	}

	/* the issue is resolved, finish the issue take up new issue if it is avaiable*/
	public void issueCompleted() {
		currentIssue = null;
		assignNewIssue();
	}



	/* Assign a new issue to an faculty, if the faculty is free. */
	public boolean assignNewIssue() {
		if (isFree()) {
			return issueHandler.assignCall(this);
		}else {
			return false;
		}
	}

	/* Returns whether or not the faculty is free. */
	public boolean isFree() {
		if (currentIssue == null) {
			return true;
		}
		return false;
	}

	public Rank getRank() {
		return this.r;
	}
}
