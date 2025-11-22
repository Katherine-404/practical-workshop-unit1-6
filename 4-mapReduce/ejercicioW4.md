## Group 12: Automated Document Sorting and Retrieval System (MapReduce Scale)																
																
**Domain Focus:** Enterprise-scale document management processing petabytes of corporate documents for intelligent organization and retrieval across global organizations.																
																
**Core Challenge:** Process massive document repositories from multinational corporations to implement intelligent document classification, enable advanced search capabilities, and provide personalized content recommendations using distributed information retrieval and knowledge management systems.																
																
**MapReduce Implementation Requirements:**																
																
### **Algorithm 1: Document Type Counter (Basic Counting)**																
- **Map Function**: Read document metadata, emit (document_type, 1)																
- **Reduce Function**: Count total documents per type (PDF, Word, Excel, etc.)																
- **Goal**: Find which document types are most common in the system																
- **Hint**: Count document types like counting words, but group by file type																
																
### **Algorithm 2: Average Document Size Calculator (Simple Aggregation)**																
- **Map Function**: Read document data, emit (department, file_size)																
- **Reduce Function**: Calculate average document size per department																
- **Goal**: Find which departments create largest vs smallest documents																
- **Hint**: Add up file sizes for each department, divide by number of documents																
																
### **Algorithm 3: Document Report Generator (Basic Join)**																
- **Map Function**: Read document data and user data, emit (document_id, data_with_type)																
- **Reduce Function**: Combine document info with author information																
- **Goal**: Create reports showing document creation by user/department																
- **Hint**: Match documents with their authors and metadata																
																
### **Algorithm 4: Document System Costs**																
- Calculate costs of storing different numbers of documents																
- Compare storage needs for different file types and sizes																
- Estimate processing costs for different organization sizes																
- **Goal**: Understand costs of enterprise document management																
																
### **Algorithm 5: Document Processing Performance**																
- Test document analysis with different cluster sizes																
- Compare processing time for small vs large document collections																
- Measure system performance during peak document creation periods																
- **Goal**: See how system handles document processing loads																
																
**Unit 4 MapReduce Extensions (Add to existing Unit 3 Documents JSON):**																
																
**New fields to add:**																
``json					
{								
// ... existing Unit 3 Documents JSON fields remain unchanged ...																
																
// MapReduce-specific fields added for Unit 4:		

mapReducePartition: '{{integer(1, 25)}}',																
processingNode: 'node_{{integer(1, 12)}}',																
batchId: 'batch_{{integer(1000, 9999)}}',																
aggregationKey: '{{documentType}}_{{department}}'																
																
// ... rest of existing Unit 3 fields continue unchanged ...																
}																
``															
																
**Integration Instructions:**																
- Add these fields to the existing Unit 3 Documents JSON structure																
- Keep all existing nested objects (`accessPatterns`, `userWorkflows`, `contentSimilarity`, `retrievalMetrics`, etc.)																
- Maintain Unit 3 record count																
``															
																
**Dataset Scope:** 1,000 corporate document records with metadata and user information.																
																
															