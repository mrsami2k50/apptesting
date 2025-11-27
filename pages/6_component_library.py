"""
Component Library - Functional Legos
Each block shows what it is, what it needs, and how it connects.
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.state import init_state, get_project
from utils.content import COMPONENT_EXPLANATIONS

st.set_page_config(
    page_title="component library | fullshtack",
    page_icon="",
    layout="wide"
)

# Initialize
init_state()
project = get_project()

# Custom CSS for component previews
st.markdown("""
<style>
    .component-card {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        background: #fafafa;
    }
    .component-preview {
        background: white;
        border: 1px solid #ddd;
        border-radius: 4px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .dependency-tag {
        display: inline-block;
        background: #e3f2fd;
        color: #1976d2;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
        margin-right: 0.5rem;
    }
    .prop-tag {
        display: inline-block;
        background: #fff3e0;
        color: #e65100;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
        margin-right: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("## component library")
st.markdown("*functional legos - each one shows what it is, what it needs, what it connects to*")

st.markdown("""
These aren't just pretty pictures of UI elements.

Each component here is a **contract**:
- What data does it expect?
- What does it do with that data?
- What happens when things go wrong?
- How does it talk to other components?

Click any component to see the full picture.
""")

st.markdown("---")

# Component categories
COMPONENTS = {
    "inputs": {
        "name": "getting input from people",
        "items": [
            {
                "name": "Text Input",
                "description": "a box where someone types something",
                "props": ["label", "placeholder", "value", "onChange", "validation"],
                "dependencies": [],
                "connects_to": ["Forms", "State"],
                "preview_html": """
                    <div style="margin: 1rem 0;">
                        <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Email address</label>
                        <input type="email" placeholder="you@example.com" style="width: 100%; padding: 0.75rem; border: 1px solid #ddd; border-radius: 4px; font-size: 1rem;">
                    </div>
                """,
                "code_example": """
// What this looks like in your code
<TextInput
  label="Email address"
  placeholder="you@example.com"
  value={email}
  onChange={(e) => setEmail(e.target.value)}
  validation={{
    required: true,
    pattern: /^[^@]+@[^@]+$/,
    errorMessage: "that doesn't look like an email"
  }}
/>
                """,
                "gotchas": "Always validate on the server too. The browser can be tricked."
            },
            {
                "name": "Password Input",
                "description": "like text input but hidden, with optional show/hide toggle",
                "props": ["label", "value", "onChange", "showToggle", "minLength"],
                "dependencies": [],
                "connects_to": ["Forms", "Auth"],
                "preview_html": """
                    <div style="margin: 1rem 0;">
                        <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Password</label>
                        <input type="password" value="secretpassword" style="width: 100%; padding: 0.75rem; border: 1px solid #ddd; border-radius: 4px; font-size: 1rem;">
                    </div>
                """,
                "code_example": """
<PasswordInput
  label="Password"
  value={password}
  onChange={(e) => setPassword(e.target.value)}
  showToggle={true}
  minLength={8}
  requirements={["uppercase", "number"]}
/>
                """,
                "gotchas": "Never store passwords in plain text. Your auth system handles this."
            },
            {
                "name": "Select / Dropdown",
                "description": "pick one thing from a list of things",
                "props": ["label", "options", "value", "onChange", "placeholder"],
                "dependencies": [],
                "connects_to": ["Forms", "State", "API (for dynamic options)"],
                "preview_html": """
                    <div style="margin: 1rem 0;">
                        <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Category</label>
                        <select style="width: 100%; padding: 0.75rem; border: 1px solid #ddd; border-radius: 4px; font-size: 1rem;">
                            <option>Choose a category...</option>
                            <option>Electronics</option>
                            <option>Clothing</option>
                            <option>Home & Garden</option>
                        </select>
                    </div>
                """,
                "code_example": """
<Select
  label="Category"
  placeholder="Choose a category..."
  options={categories}  // from your database
  value={selectedCategory}
  onChange={(value) => setSelectedCategory(value)}
/>
                """,
                "gotchas": "Options often come from your database. Handle the loading state."
            },
            {
                "name": "Checkbox",
                "description": "yes or no. on or off. true or false.",
                "props": ["label", "checked", "onChange", "disabled"],
                "dependencies": [],
                "connects_to": ["Forms", "State"],
                "preview_html": """
                    <div style="margin: 1rem 0;">
                        <label style="display: flex; align-items: center; cursor: pointer;">
                            <input type="checkbox" checked style="margin-right: 0.5rem; width: 1rem; height: 1rem;">
                            <span>I agree to the terms</span>
                        </label>
                    </div>
                """,
                "code_example": """
<Checkbox
  label="I agree to the terms"
  checked={agreedToTerms}
  onChange={(e) => setAgreedToTerms(e.target.checked)}
/>
                """,
                "gotchas": "For 'required' checkboxes (like terms), validate before form submit."
            }
        ]
    },
    "actions": {
        "name": "things people click",
        "items": [
            {
                "name": "Button",
                "description": "a clickable thing that does something when clicked",
                "props": ["label", "onClick", "type", "disabled", "loading"],
                "dependencies": [],
                "connects_to": ["Forms", "API calls", "Navigation"],
                "preview_html": """
                    <div style="margin: 1rem 0; display: flex; gap: 0.5rem;">
                        <button style="background: #0066FF; color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 4px; cursor: pointer; font-size: 1rem;">Save changes</button>
                        <button style="background: white; color: #333; border: 1px solid #ddd; padding: 0.75rem 1.5rem; border-radius: 4px; cursor: pointer; font-size: 1rem;">Cancel</button>
                    </div>
                """,
                "code_example": """
<Button
  onClick={handleSave}
  loading={isSaving}
  disabled={!isValid}
>
  Save changes
</Button>

// The onClick should handle:
// 1. Sending data to your API
// 2. Showing loading state
// 3. Handling success (show message, redirect)
// 4. Handling errors (show what went wrong)
                """,
                "gotchas": "Buttons inside forms submit the form. Add type='button' if you don't want that."
            },
            {
                "name": "Link Button",
                "description": "looks like a button, but goes somewhere instead of doing something",
                "props": ["href", "label", "variant"],
                "dependencies": ["Router"],
                "connects_to": ["Pages", "Navigation"],
                "preview_html": """
                    <div style="margin: 1rem 0;">
                        <a href="#" style="display: inline-block; background: #0066FF; color: white; text-decoration: none; padding: 0.75rem 1.5rem; border-radius: 4px; font-size: 1rem;">Go to dashboard</a>
                    </div>
                """,
                "code_example": """
<LinkButton href="/dashboard">
  Go to dashboard
</LinkButton>

// For external links, add target="_blank" and rel="noopener"
                """,
                "gotchas": "For internal navigation, use your framework's Link component for faster page loads."
            }
        ]
    },
    "layout": {
        "name": "organizing stuff on the page",
        "items": [
            {
                "name": "Card",
                "description": "a contained box that groups related content together",
                "props": ["children", "title", "footer", "onClick"],
                "dependencies": [],
                "connects_to": ["Lists", "Grids", "Data display"],
                "preview_html": """
                    <div style="border: 1px solid #ddd; border-radius: 8px; overflow: hidden; max-width: 300px; margin: 1rem 0;">
                        <div style="background: #f5f5f5; height: 150px; display: flex; align-items: center; justify-content: center; color: #999;">image</div>
                        <div style="padding: 1rem;">
                            <h4 style="margin: 0 0 0.5rem 0;">Product Name</h4>
                            <p style="margin: 0; color: #666; font-size: 0.9rem;">A brief description of this item that might wrap to two lines.</p>
                            <p style="margin: 0.5rem 0 0 0; font-weight: bold;">$99.00</p>
                        </div>
                    </div>
                """,
                "code_example": """
<Card onClick={() => goToProduct(product.id)}>
  <Card.Image src={product.image} alt={product.name} />
  <Card.Body>
    <Card.Title>{product.name}</Card.Title>
    <Card.Text>{product.description}</Card.Text>
    <Card.Price>{product.price}</Card.Price>
  </Card.Body>
</Card>
                """,
                "gotchas": "Keep cards in a grid consistent - same info in same positions."
            },
            {
                "name": "Navigation",
                "description": "the menu that lets people move between pages",
                "props": ["items", "currentPath", "user"],
                "dependencies": ["Router", "Auth state"],
                "connects_to": ["All pages", "Auth"],
                "preview_html": """
                    <nav style="background: #1a1a1a; padding: 1rem; display: flex; justify-content: space-between; align-items: center; border-radius: 4px; margin: 1rem 0;">
                        <div style="display: flex; gap: 2rem; align-items: center;">
                            <span style="color: white; font-weight: bold;">myapp</span>
                            <a href="#" style="color: #999; text-decoration: none;">Home</a>
                            <a href="#" style="color: white; text-decoration: none;">Products</a>
                            <a href="#" style="color: #999; text-decoration: none;">About</a>
                        </div>
                        <div>
                            <a href="#" style="color: #999; text-decoration: none;">Log in</a>
                        </div>
                    </nav>
                """,
                "code_example": """
<Nav>
  <Nav.Brand href="/">myapp</Nav.Brand>
  <Nav.Items>
    <Nav.Link href="/" active={path === "/"}>Home</Nav.Link>
    <Nav.Link href="/products" active={path === "/products"}>Products</Nav.Link>
    {user ? (
      <Nav.Link href="/profile">{user.name}</Nav.Link>
    ) : (
      <Nav.Link href="/login">Log in</Nav.Link>
    )}
  </Nav.Items>
</Nav>
                """,
                "gotchas": "Should show different options for logged-in vs logged-out users. Should indicate current page."
            },
            {
                "name": "Modal",
                "description": "a popup that appears over the page, demanding attention",
                "props": ["isOpen", "onClose", "title", "children"],
                "dependencies": [],
                "connects_to": ["Any trigger button", "Forms"],
                "preview_html": """
                    <div style="background: rgba(0,0,0,0.5); padding: 2rem; border-radius: 4px; margin: 1rem 0;">
                        <div style="background: white; border-radius: 8px; padding: 1.5rem; max-width: 400px; margin: 0 auto;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                                <h3 style="margin: 0;">Delete item?</h3>
                                <span style="cursor: pointer; font-size: 1.5rem;">&times;</span>
                            </div>
                            <p style="color: #666; margin-bottom: 1rem;">This action cannot be undone. The item will be permanently removed.</p>
                            <div style="display: flex; gap: 0.5rem; justify-content: flex-end;">
                                <button style="background: white; border: 1px solid #ddd; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer;">Cancel</button>
                                <button style="background: #dc2626; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer;">Delete</button>
                            </div>
                        </div>
                    </div>
                """,
                "code_example": """
<Modal isOpen={showDeleteModal} onClose={() => setShowDeleteModal(false)}>
  <Modal.Title>Delete item?</Modal.Title>
  <Modal.Body>
    This action cannot be undone. The item will be permanently removed.
  </Modal.Body>
  <Modal.Footer>
    <Button variant="secondary" onClick={() => setShowDeleteModal(false)}>
      Cancel
    </Button>
    <Button variant="danger" onClick={handleDelete}>
      Delete
    </Button>
  </Modal.Footer>
</Modal>
                """,
                "gotchas": "Don't overuse. Trap focus inside for accessibility. Close on escape key."
            }
        ]
    },
    "data": {
        "name": "showing data from your database",
        "items": [
            {
                "name": "Data Table",
                "description": "data organized in rows and columns, like a spreadsheet",
                "props": ["columns", "data", "onRowClick", "sortable", "pagination"],
                "dependencies": ["API / Data fetching"],
                "connects_to": ["Database", "Detail pages"],
                "preview_html": """
                    <div style="border: 1px solid #ddd; border-radius: 4px; overflow: hidden; margin: 1rem 0;">
                        <table style="width: 100%; border-collapse: collapse;">
                            <thead>
                                <tr style="background: #f5f5f5;">
                                    <th style="padding: 0.75rem; text-align: left; border-bottom: 1px solid #ddd;">Name</th>
                                    <th style="padding: 0.75rem; text-align: left; border-bottom: 1px solid #ddd;">Email</th>
                                    <th style="padding: 0.75rem; text-align: left; border-bottom: 1px solid #ddd;">Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr><td style="padding: 0.75rem; border-bottom: 1px solid #eee;">Alice Johnson</td><td style="padding: 0.75rem; border-bottom: 1px solid #eee;">alice@example.com</td><td style="padding: 0.75rem; border-bottom: 1px solid #eee;"><span style="background: #dcfce7; color: #166534; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.8rem;">Active</span></td></tr>
                                <tr><td style="padding: 0.75rem; border-bottom: 1px solid #eee;">Bob Smith</td><td style="padding: 0.75rem; border-bottom: 1px solid #eee;">bob@example.com</td><td style="padding: 0.75rem; border-bottom: 1px solid #eee;"><span style="background: #fef3c7; color: #92400e; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.8rem;">Pending</span></td></tr>
                            </tbody>
                        </table>
                    </div>
                """,
                "code_example": """
<DataTable
  columns={[
    { key: "name", label: "Name", sortable: true },
    { key: "email", label: "Email" },
    { key: "status", label: "Status", render: (val) => <StatusBadge status={val} /> }
  ]}
  data={users}  // from your API
  onRowClick={(user) => router.push(`/users/${user.id}`)}
  pagination={{ page, pageSize: 10, total }}
/>
                """,
                "gotchas": "Tables are bad on mobile. Consider card layouts for small screens. Don't load 10,000 rows."
            },
            {
                "name": "List",
                "description": "items displayed one after another, vertically",
                "props": ["items", "renderItem", "onItemClick", "emptyState"],
                "dependencies": ["API / Data fetching"],
                "connects_to": ["Database", "Detail pages"],
                "preview_html": """
                    <div style="border: 1px solid #ddd; border-radius: 4px; margin: 1rem 0;">
                        <div style="padding: 1rem; border-bottom: 1px solid #eee; display: flex; gap: 1rem; align-items: center;">
                            <div style="width: 40px; height: 40px; background: #e0e0e0; border-radius: 50%;"></div>
                            <div>
                                <div style="font-weight: 500;">New message from Alice</div>
                                <div style="color: #666; font-size: 0.9rem;">Hey, are you coming to the meeting?</div>
                            </div>
                        </div>
                        <div style="padding: 1rem; border-bottom: 1px solid #eee; display: flex; gap: 1rem; align-items: center;">
                            <div style="width: 40px; height: 40px; background: #e0e0e0; border-radius: 50%;"></div>
                            <div>
                                <div style="font-weight: 500;">Payment received</div>
                                <div style="color: #666; font-size: 0.9rem;">Order #1234 has been paid</div>
                            </div>
                        </div>
                    </div>
                """,
                "code_example": """
<List
  items={notifications}
  emptyState={<p>No notifications yet</p>}
  renderItem={(item) => (
    <List.Item onClick={() => handleNotification(item)}>
      <Avatar src={item.avatar} />
      <List.Content>
        <List.Title>{item.title}</List.Title>
        <List.Description>{item.message}</List.Description>
      </List.Content>
    </List.Item>
  )}
/>
                """,
                "gotchas": "Handle empty state. Handle loading state. For long lists, use virtualization."
            },
            {
                "name": "Empty State",
                "description": "what to show when there's nothing to show",
                "props": ["title", "description", "action"],
                "dependencies": [],
                "connects_to": ["Lists", "Tables", "Any data display"],
                "preview_html": """
                    <div style="text-align: center; padding: 3rem; background: #f9fafb; border-radius: 8px; margin: 1rem 0;">
                        <div style="font-size: 3rem; margin-bottom: 1rem;">*</div>
                        <h3 style="margin: 0 0 0.5rem 0;">No products yet</h3>
                        <p style="color: #666; margin: 0 0 1rem 0;">Create your first product to get started</p>
                        <button style="background: #0066FF; color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 4px; cursor: pointer;">Add product</button>
                    </div>
                """,
                "code_example": """
{products.length === 0 ? (
  <EmptyState
    icon="box"
    title="No products yet"
    description="Create your first product to get started"
    action={<Button onClick={() => setShowCreateModal(true)}>Add product</Button>}
  />
) : (
  <ProductGrid products={products} />
)}
                """,
                "gotchas": "Every list should have an empty state. It's a teaching moment."
            }
        ]
    },
    "forms": {
        "name": "collecting and submitting data",
        "items": [
            {
                "name": "Form",
                "description": "a container for inputs that collects data and sends it somewhere",
                "props": ["onSubmit", "children", "validation"],
                "dependencies": ["API endpoint"],
                "connects_to": ["API", "Database", "State"],
                "preview_html": """
                    <form style="max-width: 400px; margin: 1rem 0; padding: 1.5rem; border: 1px solid #ddd; border-radius: 8px;">
                        <div style="margin-bottom: 1rem;">
                            <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Email</label>
                            <input type="email" placeholder="you@example.com" style="width: 100%; padding: 0.75rem; border: 1px solid #ddd; border-radius: 4px; font-size: 1rem; box-sizing: border-box;">
                        </div>
                        <div style="margin-bottom: 1rem;">
                            <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Password</label>
                            <input type="password" style="width: 100%; padding: 0.75rem; border: 1px solid #ddd; border-radius: 4px; font-size: 1rem; box-sizing: border-box;">
                        </div>
                        <button type="submit" style="width: 100%; background: #0066FF; color: white; border: none; padding: 0.75rem; border-radius: 4px; cursor: pointer; font-size: 1rem;">Log in</button>
                    </form>
                """,
                "code_example": """
<Form onSubmit={handleLogin}>
  <Form.Field
    name="email"
    type="email"
    label="Email"
    required
  />
  <Form.Field
    name="password"
    type="password"
    label="Password"
    required
  />
  <Form.Submit loading={isLoading}>
    Log in
  </Form.Submit>
  <Form.Error error={error} />
</Form>

// The onSubmit function should:
// 1. Validate all fields
// 2. Send to API
// 3. Handle success
// 4. Handle and display errors
                """,
                "gotchas": "Always validate server-side too. Show clear error messages. Disable submit while loading."
            }
        ]
    },
    "feedback": {
        "name": "telling people what happened",
        "items": [
            {
                "name": "Alert / Toast",
                "description": "a temporary message that tells people something happened",
                "props": ["type", "message", "duration", "onClose"],
                "dependencies": [],
                "connects_to": ["Any action that needs feedback"],
                "preview_html": """
                    <div style="margin: 1rem 0;">
                        <div style="background: #dcfce7; border: 1px solid #86efac; color: #166534; padding: 1rem; border-radius: 4px; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.5rem;">
                            <span>+</span> Changes saved successfully
                        </div>
                        <div style="background: #fee2e2; border: 1px solid #fca5a5; color: #991b1b; padding: 1rem; border-radius: 4px; display: flex; align-items: center; gap: 0.5rem;">
                            <span>!</span> Something went wrong. Please try again.
                        </div>
                    </div>
                """,
                "code_example": """
// After a successful action:
toast.success("Changes saved successfully")

// After an error:
toast.error("Something went wrong. Please try again.")

// With more control:
<Alert
  type="warning"
  title="Heads up"
  message="Your trial expires in 3 days"
  action={<Button size="sm">Upgrade now</Button>}
/>
                """,
                "gotchas": "Don't stack too many. Auto-dismiss success, but let errors stick. Be specific about what happened."
            },
            {
                "name": "Loading State",
                "description": "showing that something is happening, please wait",
                "props": ["loading", "children"],
                "dependencies": [],
                "connects_to": ["Any async operation"],
                "preview_html": """
                    <div style="margin: 1rem 0; text-align: center; padding: 2rem; background: #f9fafb; border-radius: 8px;">
                        <div style="width: 40px; height: 40px; border: 3px solid #e0e0e0; border-top-color: #0066FF; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto;"></div>
                        <p style="color: #666; margin-top: 1rem;">Loading your data...</p>
                    </div>
                """,
                "code_example": """
{isLoading ? (
  <Loading message="Fetching your products..." />
) : (
  <ProductList products={products} />
)}

// Or with a wrapper:
<LoadingBoundary loading={isLoading}>
  <ProductList products={products} />
</LoadingBoundary>
                """,
                "gotchas": "Always show loading states. Skeleton loaders are better than spinners for layouts."
            }
        ]
    }
}

# Sidebar - category filter
with st.sidebar:
    st.markdown("### categories")
    selected_category = st.radio(
        "filter",
        options=["all"] + list(COMPONENTS.keys()),
        format_func=lambda x: COMPONENTS[x]["name"] if x != "all" else "all components",
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown("### your nouns")
    if project.nouns:
        for noun in project.nouns:
            st.markdown(f"- {noun.name}")
        st.caption("components can be wired to these")
    else:
        st.caption("no nouns defined yet")

    st.markdown("---")

    if st.button(" back to setup"):
        st.switch_page("pages/1_what_are_we_building.py")

# Main content
categories_to_show = [selected_category] if selected_category != "all" else COMPONENTS.keys()

for cat_key in categories_to_show:
    cat_data = COMPONENTS[cat_key]
    st.markdown(f"### {cat_data['name']}")

    for component in cat_data["items"]:
        with st.expander(f"**{component['name']}** - {component['description']}"):
            # Preview
            st.markdown("#### what it looks like")
            st.markdown(component["preview_html"], unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### what it needs (props)")
                for prop in component["props"]:
                    st.markdown(f'<span class="prop-tag">{prop}</span>', unsafe_allow_html=True)

                st.markdown("")
                st.markdown("#### connects to")
                for conn in component["connects_to"]:
                    st.markdown(f'<span class="dependency-tag">{conn}</span>', unsafe_allow_html=True)

            with col2:
                st.markdown("#### dependencies")
                if component["dependencies"]:
                    for dep in component["dependencies"]:
                        st.markdown(f"- {dep}")
                else:
                    st.caption("none - standalone component")

                st.markdown("#### watch out for")
                st.warning(component["gotchas"])

            st.markdown("#### example code")
            st.code(component["code_example"], language="jsx")

            # Connect to project nouns
            if project.nouns:
                st.markdown("#### wire to your data")
                st.markdown("this component could display or interact with:")
                cols = st.columns(len(project.nouns))
                for i, noun in enumerate(project.nouns):
                    with cols[i]:
                        st.checkbox(noun.name, key=f"{cat_key}_{component['name']}_{noun.name}")

    st.markdown("---")
