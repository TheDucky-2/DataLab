# STEP 4.b : Visualizing Missing Data 
### **(Missingness Visualization Continued)....**

In the previous steps: 

**Step 1:**  We learned what values actually count as missing (built-in + placeholders).

**Step 2:**  We explored how much data is missing at the column level.

**Step 3:**  We explored missing data at the row level.

**Step 4.a:** 

- We started exploring how we can visualize missing data with 'Easy to Understand' Bar plots.

- We also learnt about good stuff that can help us make understandable visualizations.

Now that we know about simple bar plots, we will now explore other visualization types.

## Matrix Plot:

A Matrix plot looks like "**Some chocolate bars having zebra stripes. A few of them may have too many stripes!**"

This plot shows patterns of missing data across all the rows of DataFrame.

These plots are especially useful when we want to see row-level patterns of missing data across multiple columns at once.

We can create a matrix plot of missing data by passing **'matrix'** as **viz_type** in the ``plot_missing()`` method of **MissingnessVisualizer** class.

**Example:**

    MissingnessVisualizer(df).plot_missing(viz_type = 'matrix')

**Output:**

> Here is an annotated image of **Matrix plot** used for better understanding of the plot:

![Matrix Plot of Missing Data](example_images/Matrix_Plot_of_Missing_Data.png)

We can see:

- **Bars of chocolate** having black and white zebra stripes.
- **Black** means ``data is present``, **White** means ``data is missing``.
- Column *'customer_id'* has no white stripes, which we can verify from our previous example of **Bar Plot**.
- Columns *'email'*, *'notes'* and *'phone_number'* have a good amount of missing data.
- Columns *'signup_date'* and *'event_timestamp'* have very little missing data.
- **White** lines passing through several columns in a row means **data is missing in those columns**.

> However, this image only shows a Matrix Plot of pandas **built-in missing** values.

Let us now explore what happens when we pass a list of placeholders that we consider as missing data:

## Matrix Plot - With Placeholders:

We can create a matrix plot of missing data including placeholders by passing **extra_placeholders** in the ``plot_missing()`` method of **MissingnessVisualizer** class.

**Example:**

    MissingnessVisualizer(df).plot_missing(
                viz_type = 'matrix',
                extra_placeholders = [-999, -1, '-999', '?'],    <- Passed the list of placeholders

                # Optional stuff

                title = 'Matrix Plot of Missing Data - With Placeholders', <- Title of the Plot
                title_fontsize = 30,                                       <- Title fontsize
                xlabel = 'Columns',                                        <- Label for X-axis
                xlabel_fontsize = 18,                                      <- Font size of X-axis label
                xlabel_padding = 20                                        <- Spacing around the label
    )

**Output:**

> Below is the annotated image of **Matrix plot with placeholders** used for better understanding of the plot:

![Matrix Plot of Missing Data with Placeholders](example_images/Matrix_Plot_of_Missing_Data_with_Placeholders.png)

We can see:

- These **Bars of chocolate** actually looked like they have zebra stripes, when we informed it what we consider as missing data.
- Column *'customer_id'* still has no white stripes, which means it has no missing data - **pandas built-in or placeholder values**.
- Column 'phone_number'* has a lot of missing data and is mostly gone. 
- Columns *'signup_date'* and *'event_timestamp'* still have very little missing data.
- **White** lines are very much visible now, compared to previous **Matrix Plot** with pandas built-in missing values.
- Which columns are missing together in the same rows of our data.

**Great!**

We now know:

1. How we can create a **Matrix** plot and how it helps us see patterns of missing data.

2. What missing data vs non-missing data looks like in a matrix plot (**did someone eat parts of my chocolate? if yes, from which places?**).

3. Being dependent only on built-in missing values would have resulted in missing a lot of important information we can get by including placeholders (if they exist).

4. Whether columns are missing data in same or different rows. 

Okay!

I know if one or more columns are missing values in the same rows or different rows.

But what if I want to know if there are any columns in my dataset that go missing together?

Like, "**If one column is missing data, will another column be missing data too?**"

We will look into how to visualize and identify this next.