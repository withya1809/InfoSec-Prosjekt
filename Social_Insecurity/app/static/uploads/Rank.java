package assignment2.issueresolver;

public enum Rank {
	STUDENT_ASSISTANT (0),
	PROFESSOR (1),
	HOD (2);
	
	private int value;
	
	private Rank(int v) {
		value = v;
	}
	
	public int getValue() {
		return value;
	}
}
