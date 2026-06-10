"""Example script to calculate Ixx for all AZ profiles."""

from blueprints.structural_sections.steel.standard_profiles.az import AZ

print("=" * 80)
print("AZ Profiles - Moment of Inertia (Ixx) Calculations")
print("=" * 80)

# Iterate through all AZ profiles
results = []

for profile in AZ:
    # Calculate section properties
    props = profile.section_properties(geometric=True, plastic=False, warping=False)
    
    # Get Ixx (centroidal moment of inertia about x-axis)
    ixx = props.ixx_c  # mm^4
    
    # Store results
    results.append({
        'name': profile.name,
        'area': props.area,
        'ixx': ixx,
        'iyy': props.iyy_c,
        'web_thickness': profile.web_thickness,
        'flange_thickness': profile.flange_thickness,
    })

# Sort results by profile name
results.sort(key=lambda x: x['name'])

# Print header
print(f"\n{'Profile':<20} {'Area (mm²)':<15} {'Ixx (mm⁴)':<20} {'Ixx (cm⁴)':<20} {'Iyy (mm⁴)':<20}")
print("-" * 95)

# Print results
for r in results:
    print(f"{r['name']:<20} {r['area']:>13,.0f}  {r['ixx']:>18,.0f}  {r['ixx']/1e4:>18,.2f}  {r['iyy']:>18,.0f}")

# Summary statistics
print("\n" + "=" * 80)
print("Summary Statistics")
print("=" * 80)
total_profiles = len(results)
avg_ixx = sum(r['ixx'] for r in results) / total_profiles
min_ixx = min(results, key=lambda x: x['ixx'])
max_ixx = max(results, key=lambda x: x['ixx'])

print(f"\nTotal AZ profiles: {total_profiles}")
print(f"Average Ixx: {avg_ixx:,.0f} mm⁴ ({avg_ixx/1e4:,.2f} cm⁴)")
print(f"Minimum Ixx: {min_ixx['ixx']:,.0f} mm⁴ ({min_ixx['name']})")
print(f"Maximum Ixx: {max_ixx['ixx']:,.0f} mm⁴ ({max_ixx['name']})")

print("\n" + "=" * 80)
print("Done!")
print("=" * 80)

from blueprints.structural_sections.steel.standard_profiles.az import AZ

# Access the AZ36-700N profile
profile = AZ.AZ36_700N

# Display basic profile information
print("=" * 60)
print(f"Profile: {profile.name}")
print("=" * 60)

# Basic geometry
print("\nBasic Geometry:")
print(f"  Web thickness: {profile.web_thickness} mm")
print(f"  Flange thickness: {profile.flange_thickness} mm")
print(f"  Interlocking CTC: {profile.interlocking_ctc} mm")
print(f"  Number of sheets: {profile.number_of_sheets}")

# Calculate section properties
print("\nCalculating section properties...")
props = profile.section_properties(geometric=True, plastic=True, warping=False)

# Access moment of inertia about x-axis (Ixx)
# The sectionproperties library provides ixx_c (centroidal axes)
ixx = props.ixx_c  # mm^4

print("\nSection Properties:")
print(f"  Ixx (moment of inertia about x-axis): {ixx:.2f} mm^4")