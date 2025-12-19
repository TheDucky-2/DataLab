# STEP 4: Visualization of Missing Data (Missingness Visualization)

In the previous steps, we focused on understanding what is missing data before touching the data itself:

**Step 1:** We learned what values actually count as missing (built-in + placeholders).

**Step 2:** We explored how much data is missing at the column level.

**Step 3:** We explored missing data at the row level.

Now that we understand and have explored missing data, the next natural step is to see it visually.

## What is this step about?

This step is about ``exploring missing data patterns visually``.

Instead of reading numbers or tables now, we will use simple visualizations (images) to quickly answer questions like:

- Is my missing data scattered randomly or is it in groups?

- Are some columns missing together?

- Is missingness of data increasing over time or following a pattern?

This step does not clean or modify your original data.

> However, this step does create a copy of your data and converts your placeholder values into built-in missing values.

## Why are my placeholder values converted to Pandas built-in missing values?

DataLab converts your placeholder values like **MISSING, ERROR, UNKNOWN** or anything else into **NaN** (Not a Number) automatically, for **visualization purposes only**.

This is done because DataLab uses ``missingno`` library under the hood for creating intuitive and widely-used missing data visualizations.

However, ``missingo`` only supports pandas built-in missing values, and does not consider placeholder values as missing data.

That is why all user decided missing values like:

    ['MISSING', '?', '-', 'Unknown' or anything else] are converted to -> NaN 

## Why visualize missing data Now, after so many steps?

Missing data visualization only makes sense after we know:

- What values are identified as missing

- Which placeholders represent missingness

- How missingness is distributed across rows and columns

If we jumped directly to visualization without those steps, the plots could be misleading (we will explore this too!).

That’s why DataLab follows this order:

    Understand → Explore → Visualize → Decide

## Visualizing Missing Data in DataLab

DataLab allows us to explore our missing data by creating easy to understand plots.

These plots are simple, fast, and very effective for real-world datasets.

DataLab also allows us to:

- Include both pandas missing values (NaN, NaT)

- Include our own placeholder values

However, placeholders are converted only and only for visualization (**original data remains absolutely unchanged**).

## But, what are these 'Easy to Understand' plots?

DataLab supports the most commonly used plots for visualizing missing data.

These are:

- **Bar plot** 

This looks like "**Bars of chocolates standing together, side-by-side**".

It shows how much data is missing vs how much data is not missing, per column.

- **Matrix plot**

This looks like "**Some of these chocolate bars have zebra stripes. A few of them have too many stripes!**"

This plot shows patterns of missing data across all the rows of DataFrame.

- **Heatmap**

This looks like **stairs with colors - 'red' steps mean a lot of people step there, 'blue' steps mean almost nobody does.**

This shows which columns are missing data together.

- **Dendrogram**

This looks like **matchsticks lying on a table - you keep adding the most similar ones into the same pile**.

This shows which columns have missing values in similar places.

## **DataLab Usage**

We can begin visualizing our missing data by importing ``MissingnessVisualizer`` class from datalab.

    from datalab import MissingnessVisualizer

## Bar Plot

We can create a bar plot of missing data using ``plot_missing()`` method from **MissingnessVisualizer** class.

**Example:**

    MissingnessVisualizer(df).plot_missing()

**Output:**

> Here is an annotated image of **bar plot** used for better understanding of the plot:

![Bar Plot of Missing Data](example_images/Bar_Plot_of_Missing_Data.png)

We can see:

- Column *'customer_id'* has a full bar, which means it is full and does not have missing data.
- Columns *'signup_date'* and *'event_timestamp'* have less than 500 rows missing, out of 500000.
- Columns *'email'*, *'notes'* and *'phone_number'* have a lot of missing data. 
- Column *'phone_number'* is the shortest bar of chocolate as it is missing most of the data.

## Bar Plot - With Placeholders:

--TO BE UPDATED--
