# 深入ptmalloc的细节

先来看一下这个
## GCC __builtin_expect的作用
这个指令是gcc引入的，作用是"允许程序员将最有可能执行的分支告诉编译器"。这个指令的写法为：__builtin_expect(EXP, N)。意思是：EXP==N的概率很大。

在之后的内核之旅中， 我们经常会见到这条指令的身影

## 深入堆的数据结构


之前对堆的数据结构有了一个大致的了解，但是不深入源码分析就无法进一步的理解堆实现的具体细节

我们先来看`chunk`和`mem`这两个指针的转换

如下还是`chunk`的结构体
```c
/*
  This struct declaration is misleading (but accurate and necessary).
  It declares a "view" into memory allowing access to necessary
  fields at known offsets from a given base. See explanation below.
*/
struct malloc_chunk {

  INTERNAL_SIZE_T      prev_size;  /* Size of previous chunk (if free).  */
  INTERNAL_SIZE_T      size;       /* Size in bytes, including overhead. */

  struct malloc_chunk* fd;         /* double links -- used only if free. */
  struct malloc_chunk* bk;

  /* Only used for large blocks: pointer to next larger size.  */
  struct malloc_chunk* fd_nextsize; /* double links -- used only if free. */
  struct malloc_chunk* bk_nextsize;
};
```
需要注意的是`prev_size`和`size`这两个字段合称为`chunk header`， 之后的被称为`user data`部分
每次`malloc`得到的内存指针都是指向`user data`处

这就涉及到了`chunk`指针和`mem`指针的转换
```c
/* conversion from malloc headers to user pointers, and back */
#define chunk2mem(p) ((void *) ((char *) (p) + 2 * SIZE_SZ))
#define mem2chunk(mem) ((mchunkptr)((char *) (mem) -2 * SIZE_SZ))
```
刚开始还不太明白先将p强制转化为(char *)类型的是什么意思
后来才发现是为了方便指针的加法， 因为p原本是`mchunkptr`类型的(注意`mchunkptr`本身就是指针的宏定义)， 转变为char类型是方便做指针的加减法

至于为什么是加上`2 * SIZE_SZ`，先看如下宏定义：
```c
#ifndef INTERNAL_SIZE_T
# define INTERNAL_SIZE_T size_t
#endif

/* The corresponding word size.  */
#define SIZE_SZ (sizeof (INTERNAL_SIZE_T))

/* The corresponding bit mask value.  */
#define MALLOC_ALIGN_MASK (MALLOC_ALIGNMENT - 1)
```
> 一般来说，size_t 在 64 位中是 64 位无符号整数，32 位中是 32 位无符号整数。

继续看宏定义：

**最小的chunk的大小**
```c
/* The smallest possible chunk */
#define MIN_CHUNK_SIZE (offsetof(struct malloc_chunk, fd_nextsize))
```
`offsetof`是取得偏移量，也就是取得`fd_nextsize`在chunk中的偏移量

说明最小的 chunk 至少要包含 bk 指针。

**最小申请的堆内存大小**
```c
/* The smallest size we can malloc is an aligned minimal chunk */
//MALLOC_ALIGN_MASK = 2 * SIZE_SZ -1
#define MINSIZE                                                                \
    (unsigned long) (((MIN_CHUNK_SIZE + MALLOC_ALIGN_MASK) &                   \
                      ~MALLOC_ALIGN_MASK))
```
这一段代码不是很明白其原理，放着再说
**检察给用户的内存是否对齐**
```c
/* Check if m has acceptable alignment */
// MALLOC_ALIGN_MASK = 2 * SIZE_SZ -1
#define aligned_OK(m) (((unsigned long) (m) & MALLOC_ALIGN_MASK) == 0)

#define misaligned_chunk(p)                                                    \
    ((uintptr_t)(MALLOC_ALIGNMENT == 2 * SIZE_SZ ? (p) : chunk2mem(p)) &       \
     MALLOC_ALIGN_MASK)
```

