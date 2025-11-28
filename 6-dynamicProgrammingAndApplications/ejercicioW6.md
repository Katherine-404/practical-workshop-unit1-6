## Group 12: (Exercise 7) Digital Library Search and Recommendation Engine (Near Neighbor Search Scale)

**Domain Focus:** Finding similar books and reading patterns through nearest neighbor algorithms for improved content discovery and personalized recommendations.

**Core Challenge:** Use nearest neighbor search to identify similar books, find comparable reading preferences, and discover learning patterns to enhance library services and user experience.

**Near Neighbor Search Implementation Requirements:**

### **Algorithm 1: Basic Book Similarity (Simple KNN)**
- **Problem**: Find books with similar ratings and basic characteristics
- **Distance Metric**: Euclidean distance on rating and difficulty vectors
- **Goal**: Learn KNN with basic book features
- **Hint**: Compare average ratings and reading difficulty as simple vectors

### **Algorithm 2: Genre-Based Matching (Category KNN)**
- **Problem**: Find books within similar genres and topics
- **Approach**: Group by genre and combine with rating similarity
- **Goal**: Apply KNN with categorical and numerical features
- **Hint**: Match genre first, then compare ratings and difficulty

### **Algorithm 3: Reading Level Matching (Simple User KNN)**
- **Problem**: Find books suitable for similar reader types
- **Approach**: Match books by target user type and reading time
- **Goal**: Learn simple user-based similarity
- **Hint**: Group by user type (student, casual) and reading time

### **Algorithm 4: Library KNN Performance**
- Compare KNN effectiveness for book recommendations
- Test how genre affects similarity matching quality
- **Goal**: Understand KNN parameters for library systems

### **Algorithm 5: Book Collection Grouping**
- Group books by similarity using KNN results
- Test different recommendation approaches
- **Goal**: See how KNN creates book recommendation clusters

**New fields to add to existing JSON structure (builds on Unit 5 Dynamic Programming JSON):**
```json
// Add these new fields to each existing record from Unit 5:
{
// ... existing fields from Units 1-5 ...

// Unit 6: Near Neighbor Search specific fields
librarySimilarity: {
userRatings: [
{{repeat(5)}},
{{integer(1, 5)}}'
],
genre: '{{random("Science", "History", "Literature", "Technology")}}',
difficultyLevel: '{{integer(1, 5)}}',
readingTime: '{{integer(60, 480)}}',
targetUser: '{{random("student", "casual", "professional")}}',
recommendationScore: '{{floating(0.4, 1.0, 2, "0.00")}}'
}
}
```

**Integration Instructions:**
1. Take your existing JSON from Unit 5 (Dynamic Programming)
2. Add the new `librarySimilarity` object to each record
3. Keep all previous fields from Units 1-5 intact
4. Use the enhanced records for book similarity and recommendation algorithms

**Dataset Scope:** 1,000 book records with topic vectors and reader ratings for similarity-based recommendations.