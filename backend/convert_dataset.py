import json

# Read your current dataset
with open('dataset.json', 'r', encoding='utf-8') as f:
    old_data = json.load(f)

# Convert to new format
knowledge_base = []

for key, value in old_data.items():
    # Determine category based on key
    category = "General"
    if any(word in key for word in ['admission', 'apply', 'eligibility', 'entrance', 'cutoff', 'allotment']):
        category = "Admissions"
    elif any(word in key for word in ['fee', 'scholarship', 'loan', 'payment', 'refund']):
        category = "Fees"
    elif any(word in key for word in ['hostel', 'canteen', 'transport', 'library', 'lab', 'wifi', 'classroom', 'sports', 'gym']):
        category = "Facilities"
    elif any(word in key for word in ['placement', 'internship', 'training', 'recruiting', 'companies']):
        category = "Placements"
    elif any(word in key for word in ['course', 'department', 'faculty', 'academic', 'exam']):
        category = "Academics"
    elif any(word in key for word in ['contact', 'email', 'phone', 'website', 'address']):
        category = "Contact"
    
    # Create question from key
    question = key.replace('_', ' ').title() + "?"
    
    knowledge_base.append({
        "question": question,
        "answer": value,
        "category": category
    })

# Save new format
new_data = {
    "knowledge_base": knowledge_base
}

with open('dataset.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, indent=2, ensure_ascii=False)

print(f"✅ Converted {len(knowledge_base)} entries successfully!")
print("✅ dataset.json has been updated!")