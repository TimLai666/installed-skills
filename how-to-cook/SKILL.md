---
name: how-to-cook
description: This skill provides comprehensive access to a vast collection of cooking recipes and meal planning tools. Use it to search for specific recipes, browse categories, get meal recommendations based on dietary restrictions (allergies, dislikes), or get random dish suggestions for a specific number of people. Trigger it whenever the user asks for cooking instructions, recipe ideas, or "what to eat" suggestions.
---

# How to Cook

## Overview

This skill integrates the `howtocook-mcp` server, offering a wide array of tools to assist with cooking and meal planning. It allows for detailed recipe retrieval, category-based browsing, and intelligent meal recommendations.

## Core Capabilities

### 1. Recipe Retrieval
Search for and retrieve complete recipe details, including ingredients and cooking steps.
- `get_recipe(query: string)`: Search by recipe name or ID (supports fuzzy matching).

### 2. Category Browsing
Browse recipes within specific culinary categories.
- `get_by_category(category: string)`: Valid categories include: "水产" (Seafood), "早餐" (Breakfast), "调料" (Seasoning), "甜品" (Dessert), "饮品" (Drinks), "荤菜" (Meat Dishes), "半成品加工" (Semi-finished), "汤" (Soup), "主食" (Staple Food), "素菜" (Vegetable Dishes).

### 3. Meal Recommendations & Planning
Get intelligent suggestions based on group size and dietary needs.
- `recommend_meals(peopleCount: number, allergies?: string[], avoidItems?: string[])`: Creates a weekly meal plan and a shopping list.
- `what_to_eat(peopleCount: number)`: Quick suggestions for a dish combination suitable for the specified number of people.

### 4. General Exploration
- `get_all_recipes()`: Retrieve a full list of available recipes.

## Usage

All capabilities are executed through the `scripts/howtocook.ts` script via `mcporter`.

**Example: Searching for a specific recipe**
```bash
mcporter call howtocook-mcp.mcp_howtocook_getRecipeById query="红烧肉"
```

**Example: Getting random suggestions for 2 people**
```bash
mcporter call howtocook-mcp.mcp_howtocook_whatToEat peopleCount=2
```

**Note:** The `howtocook-mcp` server must be configured in your environment (`mcporter config add howtocook-mcp ...`) for this skill to function.

## Resources

### scripts/
- `howtocook.ts`: The generated TypeScript interface for interacting with the `howtocook-mcp` server.
